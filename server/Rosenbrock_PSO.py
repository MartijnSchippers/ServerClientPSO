"""
File: Rosenbrock_PSO.py
Date: 13-01-24
Description: This script contains modifications over the PSOclass, making it suitable for the Rosenbrock function.
Author: Martijn Schippers
"""

from PSO import PSO
from Rosenbrock_particle import RosenbrockParticle
import json
import random

class RosenbrockPSO(PSO):
    """
    The RosenbrockPSO class extends the base PSO class for the Rosenbrock function optimization.

    Attributes:
        nr_particles (int): Number of particles in the swarm.
        max_generations (int): Maximum number of generations for the PSO.
        particles (list): List of RosenbrockParticle instances in the swarm.
        g_best_pos (dict): Global best position.
        g_best_value (float): Global best fitness value.
        history_fitness (list): List to store the fitness history.
    """

    def __init__(self):
        """
        Initialize a RosenbrockPSO instance.

        Notes:
            This constructor initializes the RosenbrockPSO with random particle positions.
        """
        self.history_fitness = []
        settings = json.load(open('settings.json'))
        self.nr_particles = settings["nr_particles"]
        self.max_generations = settings["nr_generations"]
        self.particles = [RosenbrockParticle(i, self.__get_rnd_val(), self.__get_rnd_val()) for i in range(self.nr_particles)]
        self.g_best_pos = self.particles[0].pos.get_position_dict()
        self.g_best_value = float('inf')
        # initialize results json file:
        self.__init_results_json_file()

    def __get_rnd_val(self):
        """
        Get a random value within a specified range.

        Returns:
            float: Random value within the specified range.
        """
        # pick a number between -2 and 2
        min_val = -2
        range_val = 4
        return min_val + random.random() * range_val

    def __init_results_json_file(self):
        """
        Initialize the results JSON file with empty data.

        Notes:
            This method creates an empty results JSON file with initial data.
        """
        # make an empty results json file
        init_data = [{"x": [], "y": [], "fitness": [], "pb": []} for _ in range(self.nr_particles)]
        with open("results.json", 'w') as f:
            f.write(json.dumps(init_data))
