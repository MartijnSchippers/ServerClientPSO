import numpy as np
from particle import Particle, Position, State
import random

class PSO:
    nr_particles = 10
    generation_nr = 0
    max_generations = 10
    particles : np.array
    g_best_pos : dict
    g_best_value : float

    def __init__(self):
        ran_nr = max(min(1.3, random.random() * 2), 0.7)
        self.particles = [Particle(i, ran_nr * 4000, ran_nr * 2000, ran_nr * 1500, 0, 0.95, 0.48) for i in range(self.nr_particles)]
        self.g_best_pos  = self.particles[0].pos.get_position_dict()
        self.g_best_value = float('inf')

    def __print_result_PSO(self):
        print("global best values: ", self.g_best_pos, " best value: ", self.g_best_value)
        for particle in self.particles:
            particle.print_history()

    def receive_random_particle_JSON(self):
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
        print(f"starting generation {self.generation_nr}")
        
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
        # check if it is not a calculation for a previous generation:
        if (self.generation_nr == generation):
            self.particles[id].update_fit_value(fit_val, run_id, self.g_best_pos)
            print("particle succesfully updated!")

        else:
            print("the generations did not match!")
            