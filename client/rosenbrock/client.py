import requests
import json
import math
import subprocess

from random import gauss
import numpy as np

class Client():
    # server_url = "http://localhost:5000/"

    def __init__(self, ip_address : str, port : str, id: str):
        self.local_id = int(id)
        self.server_url = "http://" + ip_address + ":" + port + "/rosenbrock/"
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

                # do a calculation
                answer = self.__get_calculation()

                # post answer
                if answer != None:
                    self.__post_answer(answer)
            else:
                break

    def __get_calculation(self):
        x = self.current_parameters["x"]
        y = self.current_parameters["y"]
        # rosenbrock formula
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
    
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
