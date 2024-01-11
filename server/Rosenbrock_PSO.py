from PSO import PSO
# from particle import Particle, Position, State
from Rosenbrock_particle import RosenbrockParticle
import json
import random

class RosenbrockPSO(PSO):

    def __init__(self):
        self.history_fitness = []
        x = self.__get_rnd_val()
        y = self.__get_rnd_val()
        settings = json.load(open('settings.json'))
        self.nr_particles = settings["nr_particles"]
        self.max_generations = settings["nr_generations"]
        self.particles = [RosenbrockParticle(i, x, y) for i in range(self.nr_particles)]
        self.g_best_pos  = self.particles[0].pos.get_position_dict()
        self.g_best_value = float('inf')
         # make empty results json file
        # results = {
        #     "results": [['inf'] * columns for _ in range(rows)]
        # }
        # f = open("results.json", 'w')
        # f.write(json.dumps(results))
        # f.close()

    def __get_rnd_val(self):
        #pick a number between -2 and 2
        min = -2
        range = 4
        return min + random.random() * range
    
    