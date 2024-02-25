"""
File: PSO.py
Date: 13-01-24
Description: This script contains logic for running a Particle Swarm Optimization (PSO).
Author: Martijn Schippers
"""

import json
import numpy as np
from particle import Particle, Position, State
import random

class PSO:
    """
    The PSO class represents the main logic for running a Particle Swarm Optimization (PSO).

    Attributes:
        nr_particles (int): Number of particles in the PSO.
        generation_nr (int): Current generation number.
        max_generations (int): Maximum number of generations.
        particles (np.array): Array of Particle instances.
        g_best_pos (dict): Global best position.
        g_best_value (float): Global best fitness value.
    """

    generation_nr = 0
    particles: np.array
    g_best_pos: dict
    g_best_value: float

    def __init__(self):
        """
        Initialize a PSO instance.

        Notes:
            This method initializes the particles, global best position, and global best fitness value.
        """
        #load settings
        settings = json.load(open('settings.json'))
        self.nr_particles = settings["nr_particles"]
        self.max_generations = settings["nr_generations"]
        self.noise_evals = settings["nr_noise_eval_runs"]

        # load particles
        self.particles = [
                        Particle(i, 
                            self.__get_rnd_val(2000, 8000), 
                            self.__get_rnd_val(0, 4000), 
                            self.__get_rnd_val(1000, 3000), 
                            0, # positive feedback is always 0 for testing
                            0.95, # p_c is a fixed number
                            5, # number of robots is a fixed setting
                            fill_ratio=0.48, 
                            nr_noise_eval_runs=self.noise_evals) 
                        for i in range(self.nr_particles)]
        # set postition that has the best global value
        self.g_best_pos = self.particles[0].pos.get_position_dict()
        # set the best global value (is initially infinitive)
        self.g_best_value = float('inf')

        # prepare to write into results
        self.__init_results_json_file()

    def __get_rnd_val(self, min, max):
        """
        Get a random value within a specified range, used for random initiation particle

        Returns:
            float: Random value within the specified range.
        """
        return min + random.random() * (max - min)
    
    def __print_result_PSO(self):
        """
        Print the result of the PSO, including global best values and particle histories.
        """
        print("global best values:", self.g_best_pos, "best value:", self.g_best_value)
        for particle in self.particles:
            particle.print_history()

    def receive_random_particle_JSON(self):
        """
        Receive parameters for a random particle in the PSO.

        Returns:
            str: JSON representation of parameters for a calculation run.
        """
        # check if PSO is still running
        if self.generation_nr > self.max_generations:
            return "PSO completed! Please, don't request anymore"

        # return a particle that is already running
        for particle in self.particles:
            if particle.state == State.REQUESTED:
                return particle.request_parameters_JSON(self.generation_nr)

        # all particles completely solved or unsolved, so return a particle that has not been requested yet
        for particle in self.particles:
            if particle.state == State.UNSOLVED:
                return particle.request_parameters_JSON(self.generation_nr)

        # each particle has been calculated, so the generation is complete
        print(f"GENERATION {self.generation_nr} is completed!")

        # reset particles and get new global best
        print(f"starting generation {self.generation_nr + 1}")

        for particle in self.particles:
            particle.reset()
            # update new global best
            if particle.current_fitness < self.g_best_value:
                self.g_best_pos = particle.pos.get_position_dict()
                self.g_best_value = particle.current_fitness

        # check if it was the last generation
        self.generation_nr += 1
        if self.generation_nr >= self.max_generations:
            print("SERVER: PSO completed!")
            self.__print_result_PSO()
            return "PSO completed! Please, don't request anymore"

        # return particle new generation
        return self.particles[0].request_parameters_JSON(self.generation_nr)

    def update_fitness_value(self, id, generation, run_id, fit_val):
        """
        Update fitness value for a particle in the PSO.

        Args:
            id (int): Identifier of the particle.
            generation (int): Generation number of the calculation.
            run_id (int): Identifier of the calculation run.
            fit_val (float): Fitness value for the calculation run.

        Notes:
            This method updates the fitness value for the specified particle.
        """
        # check if it is not a calculation for a previous generation:
        if (self.generation_nr == generation):
            self.particles[id].update_fit_value(fit_val, run_id, self.g_best_pos)
            print("particle successfully updated!")

        else:
            print("the generations did not match!")

    def __init_results_json_file(self):
        """
        Initialize the results JSON file with empty data.

        Notes:
            This method creates an empty results JSON file with initial data.
        """
        # make an empty results json file
        # "rw_mean": 7271.369400722904, "rw_variance": 2457.6745646676545, "tao": 1000, "u_plus": 0, "p_c": 1, "report_data": true, "nr_robots": 4}
        init_data = [{"rw_mean": [], "rw_variance": [], "tao": [], "u_plus": [], "p_c": [], "fitness": [], "pb": [], "nr_robots": []} for _ in range(self.nr_particles)]
        with open("results_webots.json", 'w') as f:
            f.write(json.dumps(init_data, indent=2))

