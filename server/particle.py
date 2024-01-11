from enum import Enum
import json
import random
from particle_run import ParticleRun
from statistics import mean

class Position:
    def __init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio):
        self.rw_mean = rw_mean
        self.rw_variance = rw_variance
        self.tao = tao
        self.u_plus = u_plus
        self.p_c = p_c
        self.fill_ratio = fill_ratio

        # WARNING: CALL THEM VIA 'get_values()', NOT DIRECTLY BY EXAMPLE pos.values
        self.values = self.get_values()

    def get_position_JSON(self):
        return json.dumps(self.values)
    
    def get_position_dict(self):
        return self.values
    
    def get_values(self):
        self.values = {
            "rw_mean": self.rw_mean,
            "rw_variance": self.rw_variance,
            "tao": self.tao,
            "u_plus": self.u_plus,
            "p_c": self.p_c,
            "fill_ratio": self.fill_ratio
        }
        return self.values

class ParticlePosition(Position):
    def __init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio = 0.48):
        Position.__init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio)
        # Initialize velocities based on a Gaussian distribution
        self.rw_mean_vel = self.__generate_variation(self.rw_mean)
        self.rw_variance_vel = self.__generate_variation(self.rw_variance)
        self.tao_vel = self.__generate_variation(self.tao)
        self.u_plus_vel = self.__generate_variation(self.u_plus)
        self.p_c_vel = self.__generate_variation(self.p_c)
        self.fill_ratio_vel =  self.__generate_variation(self.fill_ratio)

    def __generate_variation(self, value):
        return 0.5 * random.uniform(-value, value)
    
class State(Enum):
    UNSOLVED = 1
    REQUESTED = 2
    SOLVED = 3

class Particle:

    def __init__(self, id : int, rw_mean : float, rw_variance : float, tao : float, u_plus : float, p_c : float, fill_ratio = 0.48):
        self.history_fitness = []
        self.pos = ParticlePosition(rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio) # position of this particle
        self.pb = Position(rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio) # personal best
        self.id = id
        self.current_fitness = float('inf')
        self.state = State.UNSOLVED
        settings = json.load(open('settings.json'))
        self.nr_runs = settings["nr_noise_eval_runs"]
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]


    def request_parameters_JSON(self, generation : int):
        """ this is called as a request to do a calculation. Returns a current run with its parameters and sets the states to REQUESTED"""
        if self.state == State.UNSOLVED:
            self.state = State.REQUESTED

        # return an unsolved run
        for run in self.runs:
            if run.is_unsolved():
                run.set_state_to_in_progress()
                return self._return_parameters(generation, run.id)
            
        # all runs are (being) solved, so return a run that is already being requested
        for run in self.runs:
            if run.is_in_progress():
                return self._return_parameters(generation, run.id)
            
        # return an error instead
        return "there is an error: all runs of this particle already have been calculated, but the state of this particle is not updated"
        
    
    def print_history(self):
        self.history_fitness.append(self.current_fitness)
        print("Particle id = ", self.id, " with history ", *self.history_fitness)
    
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
                if fit_val < self.current_fitness:
                    self.pb = Position(self.pos.rw_mean, self.pos.rw_variance, self.pos.tao, self.pos.u_plus, self.pos.p_c, self.pos.fill_ratio)
                
                #update velocity
                self.pos.rw_mean_vel += self._update_variable(self.pos.rw_mean_vel, self.pos.rw_mean, self.pb.rw_mean, gb["rw_mean"])
                self.pos.rw_variance_vel += self._update_variable(self.pos.rw_variance_vel, self.pos.rw_variance, self.pb.rw_variance, gb["rw_variance"])
                self.pos.tao_vel += self._update_variable(self.pos.tao_vel, self.pos.tao, self.pb.tao, gb["tao"])
                self.pos.u_plus_vel += self._update_variable(self.pos.u_plus_vel, self.pos.u_plus, self.pb.u_plus, gb["u_plus"])
                self.pos.p_c_vel = self._update_variable(self.pos.p_c_vel, self.pos.p_c, self.pb.p_c, gb["p_c"])
                self.pos.fill_ratio_vel += self._update_variable(self.pos.fill_ratio_vel, self.pos.fill_ratio, self.pb.fill_ratio, gb["fill_ratio"])
                
                # set fitness value to up to date
                self.state = State.SOLVED

    def reset(self):
        # update position
        self.history_fitness.append(self.current_fitness)
        self.pos.rw_mean += self.pos.rw_mean_vel
        self.pos.rw_mean = max(1000, min(8000, self.pos.rw_mean))

        # WARNING! VARIANCE IS NOT YET IMPLEMENTED IN CLIENT WEBOTS!
        self.pos.rw_variance += self.pos.rw_variance_vel
        self.pos.rw_variance = max(0, min(4000, self.pos.rw_variance))

        self.pos.tao += self.pos.tao_vel
        self.pos.tao = max(1000, min(3000, self.pos.tao))

        self.pos.p_c += self.pos.p_c_vel
        self.pos.p_c = max(0.85, min(0.99, self.pos.p_c))

        # set new value to be not up to date
        self.state = State.UNSOLVED
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]

    def _return_parameters(self, generation, run_id):
        return json.dumps({"particle_id": self.id, "generation": generation, "run_id": run_id} | self.pos.get_values())
    
    def _get_avg_fitness_value(self):
        run_values = []
        for run in self.runs:
            run_values.append(run.answer)
        return mean(run_values)
    
    def _all_runs_have_been_calculated(self):
        for run in self.runs:
            if not run.is_solved():
                return False
        return True
    
    def _update_variable(self, old_vel, old_value, personal_best, global_best):
        # PSO_W = -0.1832 # PSO Parameters
        # PSO_PW = 0.5287
        # PSO_NW = 3.1913

        PSO_W = 0.8 # PSO Parameters
        PSO_PW = 0.1
        PSO_NW = 0.1

        r1 = random.random()
        r2 = random.random()
        return PSO_W * old_vel + PSO_PW * r1 * (personal_best - old_value) + PSO_NW * r2 * (global_best - old_value)