import requests
import json
import math
import os
import subprocess

from random import gauss
from world_generation.createWorldParallel import WorldGenerator
import numpy as np

class Client():
    # server_url = "http://localhost:5000/"

    def __init__(self, ip_address : str, port : str, id: str):
        self.local_id = int(id)
        self.server_url = "http://" + ip_address + ":" + port + "/"
        self.request_comp_url = self.server_url + "compute"
        self.post_ans_url= self.server_url + "submit"
        self.current_parameters = {}
        self.particle_id : int
        self.particle_generation : int
        self.run_id : int
        return
    
    def run(self):
        # main loop
        while(True):
            # request to do a computation
            if self.__request_computation() == True:
                # get the right settings
                self.particle_id = self.current_parameters["particle_id"]
                self.particle_generation = self.current_parameters["generation"]
                self.run_id = self.current_parameters["run_id"]
                nr_robots = self.current_parameters["nr_robots"]

                # create an arena
                self.__create_arena(nr_robots)

                # do a calculation
                answer = self.__do_calculation()

                # post answer
                if answer != None:
                    self.__post_answer(answer)
            else:
                break

    def __create_arena(self, nr_robots):
        wg = WorldGenerator(fill_ratio = 0.48, instance_id=self.run_id, robot_number=nr_robots)
        wg.createWorld()

    def __do_calculation(self):
        # make parameters.json and put them on the right place
        values = {
            "rw_mean" : self.current_parameters["rw_mean"],
            "rw_variance": self.current_parameters["rw_variance"],
            "tao": self.current_parameters["tao"],
            "u_plus": self.current_parameters["u_plus"],
            "p_c": self.current_parameters["p_c"],
            "report_data" : False,
            "nr_robots" : self.current_parameters["nr_robots"]
        }
        demo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../")
        controller_path = os.path.join(demo_path, "controllers/")
        with open(controller_path + "bayesV2/parameters_" + str(self.local_id) + ".json", 'w') as para_file:
            json.dump(values, para_file)

        # launch webots
        # worlds_path = os.path.join(demo_path, "worlds")
        command = ["webots", "--mode=fast", "--no-rendering", demo_path + "worlds/bayes_pso_0_" + str(0) + ".wbt"]

        # Use subprocess.run with the list of strings
        subprocess.run(command)

        # return answer of supervisor, otherwise, return an error
        
        try:
            with open(controller_path + 'cpp_supervisor/local_fitness_' + str(self.local_id) + '.txt', 'r') as file:
                # Do something with the file, such as reading its content
                fitness_value = file.readline().strip()
                return float(fitness_value)
        except FileNotFoundError:
            print("The file does not exist.")
    
    def __post_answer(self, answer):
        # return the dictionary as json to the post url
        response = requests.post(self.post_ans_url, json = {
            'particle_id' : self.particle_id, 
            'generation': self.particle_generation, 
            'run_id': self.run_id,
            'answer': answer
            } )
        
        # Check the response
        if response.status_code == 200:
            print("SERVER: ", response.text)
            return True
        else:
            print("The server did not give a confirmation about the answer")
            return False
    
    def __request_computation(self):
        # Send a POST request to the server
        response = requests.get(self.request_comp_url)

        # Check the response
        if response.status_code == 200:
            try:
                self.current_parameters = response.json()
                print("Computation result:", self.current_parameters)
            except:
                print(response.text)
                return False
            return True
        else:
            print("Error:", response.status_code, response.text)
            return False
