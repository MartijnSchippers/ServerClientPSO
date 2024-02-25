"""
File: particle.py
Date: 13-01-24
Description: This script contains information about the particles.
Author: Martijn Schippers
"""

from enum import Enum
import json
import random
from particle_run import ParticleRun
from statistics import mean

class Position:
    """
    The Position class represents a position in the particle's parameter space.

    Attributes:
        rw_mean (float): Mean of random walk parameter.
        rw_variance (float): Variance of random walk parameter.
        tao (float): Tau parameter.
        u_plus (float): U plus parameter.
        p_c (float): Probability of communication parameter.
        fill_ratio (float): Fill ratio parameter.
        values (dict): Dictionary representation of position values.
    """

    def __init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio, nr_robots):
        """
        Initialize a Position instance.

        Args:
            rw_mean (float): Mean of random walk parameter.
            rw_variance (float): Variance of random walk parameter.
            tao (float): Tau parameter.
            u_plus (float): U plus parameter.
            p_c (float): Probability of communication parameter.
            fill_ratio (float): Fill ratio parameter.
        """
        self.rw_mean = rw_mean
        self.rw_variance = rw_variance
        self.tao = tao
        self.u_plus = u_plus
        self.p_c = p_c
        self.fill_ratio = fill_ratio
        self.nr_robots = nr_robots

        # WARNING: CALL THEM VIA 'get_values()', NOT DIRECTLY BY EXAMPLE pos.values
        self.values = self.get_values()

    def get_position_JSON(self):
        """
        Get the JSON representation of the position.

        Returns:
            str: JSON representation of the position.
        """
        return json.dumps(self.get_values())
    
    def get_position_dict(self):
        """
        Get the dictionary representation of the position.

        Returns:
            dict: Dictionary representation of the position.
        """
        return self.values
    
    def get_values(self):
        """
        Get the dictionary representation of the position.

        Returns:
            dict: Dictionary representation of the position.
        """
        self.values = {
            "rw_mean": self.rw_mean,
            "rw_variance": self.rw_variance,
            "tao": self.tao,
            "u_plus": bool(self.u_plus),
            "p_c": self.p_c,
            "fill_ratio": self.fill_ratio,
            "nr_robots": int(self.nr_robots) # IMPORTANT: rounds a float down to an int (cannot have 4.2 robots e.g.)
        }
        return self.values

class ParticlePosition(Position):
    """
    The ParticlePosition class represents the position of a particle in the parameter space.

    Attributes:
        rw_mean_vel (float): Velocity for random walk mean.
        rw_variance_vel (float): Velocity for random walk variance.
        tao_vel (float): Velocity for tau parameter.
        u_plus_vel (float): Velocity for U plus parameter.
        p_c_vel (float): Velocity for probability of communication parameter.
        fill_ratio_vel (float): Velocity for fill ratio parameter.
    """

    def __init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio, nr_robots):
        """
        Initialize a ParticlePosition instance.

        Args:
            rw_mean (float): Mean of random walk parameter.
            rw_variance (float): Variance of random walk parameter.
            tao (float): Tau parameter.
            u_plus (float): U plus parameter.
            p_c (float): Probability of communication parameter.
            fill_ratio (float, optional): Fill ratio parameter. Defaults to 0.48.
        """
        Position.__init__(self, rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio, nr_robots)
        # Initialize velocities based on a Gaussian distribution
        self.rw_mean_vel = self.__generate_variation(self.rw_mean)
        self.rw_variance_vel = self.__generate_variation(self.rw_variance)
        self.tao_vel = self.__generate_variation(self.tao)
        # self.u_plus_vel = self.__generate_variation(self.u_plus)
        self.u_plus_vel = 0 # u_plus does not change
        self.p_c_vel = self.__generate_variation(self.p_c)
        self.fill_ratio_vel = self.__generate_variation(self.fill_ratio)
        self.nr_robots_vel = self.__generate_variation(self.nr_robots)

    def __generate_variation(self, value):
        """
        Generate a random variation for a given value.

        Args:
            value (float): The original value.

        Returns:
            float: Randomly varied value.
        """
        return 0.1 * random.uniform(-value, value)

class State(Enum):
    """
    Enumeration representing the possible states of a Particle instance.

    Attributes:
        UNSOLVED (int): State indicating the particle is unsolved.
        REQUESTED (int): State indicating a calculation request has been made.
        SOLVED (int): State indicating the particle is solved.
    """
    UNSOLVED = 1
    REQUESTED = 2
    SOLVED = 3

    
class State(Enum):
    UNSOLVED = 1
    REQUESTED = 2
    SOLVED = 3

"""
File: particle.py
Date: 13-01-24
Description: This script contains the Particle class representing a particle in the Particle Swarm Optimization (PSO) algorithm.
Author: Martijn Schippers
"""

class Particle:
    """
    The Particle class represents a particle in the Particle Swarm Optimization (PSO) algorithm.

    Attributes:
        history_fitness (list): List of historical fitness values.
        pos (ParticlePosition): Current position of the particle.
        pb (Position): Personal best position.
        id (int): Identifier for the particle.
        current_fitness (float): Current fitness value.
        state (State): Current state of the particle (UNSOLVED, REQUESTED, SOLVED).
        nr_runs (int): Number of noise evaluation runs.
        runs (list): List of ParticleRun instances.
    """

    def __init__(self, id, rw_mean, rw_variance, tao, u_plus, p_c, nr_robots, fill_ratio=0.48, nr_noise_eval_runs = 10):
        """
        Initialize a Particle instance.

        Args:
            id (int): Identifier for the particle.
            rw_mean (float): Mean of random walk parameter.
            rw_variance (float): Variance of random walk parameter.
            tao (float): Tau parameter.
            u_plus (float): U plus parameter.
            p_c (float): Probability of communication parameter.
            fill_ratio (float, optional): Fill ratio parameter. Defaults to 0.48.
        """
        self.history_fitness = []
        print("nr_robots: ", nr_robots)
        self.pos = ParticlePosition(rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio, nr_robots)  # position of this particle
        self.pb = Position(rw_mean, rw_variance, tao, u_plus, p_c, fill_ratio, nr_robots)  # personal best
        self.id = id
        self.current_fitness = self.pb_value = float('inf')
        self.state = State.UNSOLVED
        self.nr_runs = nr_noise_eval_runs
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]
        print(self.pos.get_values())

    def request_parameters_JSON(self, generation):
        """
        Request parameters for a calculation.

        Args:
            generation (int): Current generation number.

        Returns:
            str: JSON representation of parameters for a calculation run.
        """
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
        """
        Print the history of fitness values for the particle.
        """
        self.history_fitness.append(self.current_fitness)
        print("Particle id =", self.id, "with history", *self.history_fitness)

    def update_fit_value(self, fit_val, run_id, gb: dict):
        """
        Update fitness value for the particle, regardsless of which run is chosen

        Args:
            fit_val (float): New fitness value.
            run_id (int): Identifier of the run.
            gb (dict): Global best values.

        Notes:
            This method updates the fitness value, personal best, and velocity of the particle.
        """
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
                print("done for particle with id:", self.id)
                # update fitness value this particle
                self.current_fitness = self._get_avg_fitness_value()

                # update personal best if applied
                if self.current_fitness < self.pb_value:
                    self.pb = Position(self.pos.rw_mean, self.pos.rw_variance, self.pos.tao, self.pos.u_plus, self.pos.p_c, self.pos.fill_ratio, self.pos.nr_robots)
                    self.pb_value = self.current_fitness

                # update velocity
                self.pos.rw_mean_vel = self._update_variable(self.pos.rw_mean_vel, self.pos.rw_mean, self.pb.rw_mean, gb["rw_mean"])
                self.pos.rw_variance_vel = self._update_variable(self.pos.rw_variance_vel, self.pos.rw_variance, self.pb.rw_variance, gb["rw_variance"])
                self.pos.tao_vel = self._update_variable(self.pos.tao_vel, self.pos.tao, self.pb.tao, gb["tao"])
                # self.pos.u_plus_vel = self._update_variable(self.pos.u_plus_vel, self.pos.u_plus, self.pb.u_plus, gb["u_plus"])
                self.pos.p_c_vel = self._update_variable(self.pos.p_c_vel, self.pos.p_c, self.pb.p_c, gb["p_c"])
                self.pos.fill_ratio_vel = self._update_variable(self.pos.fill_ratio_vel, self.pos.fill_ratio, self.pb.fill_ratio, gb["fill_ratio"])
                # self.pos.nr_robots_vel = self._update_variable(self.pos.nr_robots_vel, self.pos.nr_robots, self.pb.nr_robots, gb["nr_robots"])
                self.pos.nr_robots_vel = 0 # is a fixed number now
                # set fitness value to up to date
                self.state = State.SOLVED

    def reset(self):
        """
        This is called by the PSO script when all particles performed all runs. 
        Reset the particle to its initial state. Also write down the results of the run. 

        Notes:
            This method updates the position, fitness history, and resets the state of the particle.
        """
        # update position
        self.history_fitness.append(self.current_fitness)
        with open("results_webots.json", 'r') as f:
            values = json.load(f)
            # "rw_mean": 7271.369400722904, "rw_variance": 2457.6745646676545, "tao": 1000, "u_plus": 0, "p_c": 1, "report_data": true, "nr_robots": 4}
            values[self.id]["fitness"].append(self.current_fitness)
            values[self.id]["rw_mean"].append(self.pos.rw_mean)
            values[self.id]["rw_variance"].append(self.pos.rw_variance)
            values[self.id]["tao"].append(self.pos.tao)
            values[self.id]["u_plus"].append(self.pos.u_plus)
            values[self.id]["p_c"].append(self.pos.p_c)
            values[self.id]["nr_robots"].append(self.pos.nr_robots)
            values[self.id]["pb"].append(self.pb_value)      

        with open("results_webots.json", 'w') as f:
            f.write(json.dumps(values, indent=2))
            f.close()

        self.pos.rw_mean += self.pos.rw_mean_vel
        self.pos.rw_mean = max(2000, min(8000, self.pos.rw_mean))

        # WARNING! VARIANCE IS NOT YET IMPLEMENTED IN CLIENT WEBOTS!
        self.pos.rw_variance += self.pos.rw_variance_vel
        self.pos.rw_variance = max(0, min(4000, self.pos.rw_variance))

        self.pos.tao += self.pos.tao_vel
        self.pos.tao = max(1000, min(3000, self.pos.tao))

        self.pos.p_c += self.pos.p_c_vel
        self.pos.p_c = max(0.85, min(0.99, self.pos.p_c))

        self.pos.nr_robots += self.pos.nr_robots_vel
        self.pos.nr_robots = max(2, min(10, self.pos.nr_robots))

        # set new value to be not up to date
        self.state = State.UNSOLVED
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]

    def _return_parameters(self, generation, run_id):
        """
        Return the parameters in JSON format for a calculation run.

        Args:
            generation (int): Current generation number.
            run_id (int): Identifier of the run.

        Returns:
            str: JSON representation of parameters for a calculation run.
        """
        dump = {"particle_id": self.id, "generation": generation, "run_id": run_id}
        dump.update(self.pos.get_values())
        return json.dumps(dump)

    def _get_avg_fitness_value(self):
        """
        Calculate the average fitness value of all runs.

        Returns:
            float: Average fitness value.
        """
        run_values = [run.answer for run in self.runs]
        return mean(run_values)

    def _all_runs_have_been_calculated(self):
        """
        Check if all runs for the particle have been solved.

        Returns:
            bool: True if all runs are solved, False otherwise.
        """
        return all(run.is_solved() for run in self.runs)

    def _update_variable(self, old_vel, old_value, personal_best, global_best):
        """
        Update a variable based on PSO parameters.

        Args:
            old_vel (float): Old velocity value.
            old_value (float): Old variable value.
            personal_best (float): Personal best value.
            global_best (float): Global best value.

        Returns:
            float: Updated velocity value.
        """
        # PSO_W = -0.1832 # PSO Parameters
        # PSO_PW = 0.5287
        # PSO_NW = 3.1913

        PSO_W = 0.75  # PSO Parameters
        PSO_PW = 2.25
        PSO_NW = 1.5

        r1 = random.random()
        r2 = random.random()
        return PSO_W * old_vel + PSO_PW * r1 * (personal_best - old_value) + PSO_NW * r2 * (global_best - old_value)
