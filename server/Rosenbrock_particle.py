from particle import Particle, State
from particle_run import ParticleRun
import json
import random

class RosenbrockPosition:
    def __init__(self, x, vel_x, y, vel_y):
        self.x = x
        self.vel_x = vel_x
        self.y = y
        self.vel_y = vel_y
        self.values = self.get_values()
       


    def get_position_JSON(self):
        return json.dumps(self.values)
    
    def get_position_dict(self):
        return self.values
    
    def get_values(self):
        self.values = {
            "x": self.x,
            "y": self.y
        }
        return self.values


class RosenbrockParticle(Particle):
    def __init__(self, id, x, y):
        self.history_fitness = []
        self.pos = RosenbrockPosition(x, random.random(), y, random.random())
        self.pb = self.pos
        self.id = id
        self.current_fitness = float('inf')
        self.pb_fitness = self.current_fitness
        self.state = State.UNSOLVED
        settings = json.load(open('settings.json'))
        self.nr_runs = settings["nr_noise_eval_runs"]
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]

    def update_fit_value(self, fit_val, run_id, gb : dict):
        # TODO: rename to 'update_particle'
        # check if particle is already solved
        if not self.state == State.SOLVED:
            # update the right run of this particle
            for run in self.runs:
                if run.id == run_id:
                    # we have the right run, now update the fitness value
                    run.update_fit_value(fit_val)
                    break
            
            # check if all runs have been solved
            if self._all_runs_have_been_calculated():
                print("done for particle with id: ", self.id)
                # update fitness value this particle
                self.current_fitness = self._get_avg_fitness_value()

                # update personal best if applied
                # TODO: make this right in the Webots PSO!!!!!
                if fit_val < self.pb_fitness:
                    self.pb = self.pos
                    self.pb_fitness = fit_val
                
                #update velocity_update_variable(self, old_vel, old_value, personal_best, global_best)
                self.pos.vel_x = self._update_variable(self.pos.vel_x, self.pos.x, self.pb.x, gb["x"])
                # self.pos.vel_y += self._update_variable(self.pos.vel_y, self.pos.y, self.pb.y, gb["y"])
                self.pos.vel_y = self._update_variable(self.pos.vel_y, self.pos.y, self.pb.x, gb["y"])
                
                # set fitness value to up to date
                self.state = State.SOLVED

    def reset(self):
        # update position
        self.history_fitness.append(self.current_fitness)
        with open("results.json", 'r') as f:
            values = json.load(f)
            values[self.id]["fitness"].append(self.current_fitness)
            values[self.id]["x"].append(self.pos.x)
            values[self.id]["y"].append(self.pos.y)
            values[self.id]["pb"].append(self.pb_fitness)


        with open("results.json", 'w') as f:
            f.write(json.dumps(values, indent = 2))
            f.close()
        
        self.pos.x += self.pos.vel_x
        self.pos.y += self.pos.vel_y

        # set new value to be not up to date
        self.state = State.UNSOLVED
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]

