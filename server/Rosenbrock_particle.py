"""
File: Rosenbrock_particle.py
Date: 13-01-24
Description: This script contains modifications over the particle class, making it suitable for the Rosenbrock function.
Author: Martijn Schippers
"""

from particle import Particle, State
from particle_run import ParticleRun
import json
import random

class RosenbrockPosition:
    """
    The RosenbrockPosition class represents the position of a particle in the Rosenbrock function.

    Attributes:
        x (float): X-coordinate.
        vel_x (float): X-coordinate velocity.
        y (float): Y-coordinate.
        vel_y (float): Y-coordinate velocity.
        values (dict): Dictionary containing X and Y coordinates.
    """

    def __init__(self, x, vel_x, y, vel_y):
        """
        Initialize a RosenbrockPosition instance.

        Args:
            x (float): X-coordinate.
            vel_x (float): X-coordinate velocity.
            y (float): Y-coordinate.
            vel_y (float): Y-coordinate velocity.
        """
        self.x = x
        self.vel_x = vel_x
        self.y = y
        self.vel_y = vel_y
        self.values = self.get_values()

    def get_position_JSON(self):
        """
        Get the JSON representation of the position.

        Returns:
            str: JSON representation of the position.
        """
        return json.dumps(self.values)

    def get_position_dict(self):
        """
        Get the dictionary representation of the position.

        Returns:
            dict: Dictionary representation of the position.
        """
        return self.values

    def get_values(self):
        """
        Get the dictionary of X and Y coordinates.

        Returns:
            dict: Dictionary with "x" and "y" as keys and corresponding coordinates as values.
        """
        self.values = {
            "x": self.x,
            "y": self.y
        }
        return self.values

class RosenbrockParticle(Particle):
    """
    The RosenbrockParticle class extends the base Particle class for the Rosenbrock function optimization.

    Attributes:
        pos (RosenbrockPosition): Position of the particle in the Rosenbrock function.
        pb (RosenbrockPosition): Personal best position.
        id (int): Identifier of the particle.
        current_fitness (float): Current fitness value of the particle.
        pb_fitness (float): Personal best fitness value.
        state (State): Current state of the particle (UNSOLVED, REQUESTED, SOLVED).
        nr_runs (int): Number of noise evaluation runs.
        runs (list): List of ParticleRun instances for each run.
    """

    def __init__(self, id, x, y):
        """
        Initialize a RosenbrockParticle instance.

        Args:
            id (int): Identifier of the particle.
            x (float): Initial X-coordinate.
            y (float): Initial Y-coordinate.
        """
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

    def update_fit_value(self, fit_val, run_id, gb: dict):
        """
        Update fitness value for a particle in the Rosenbrock function.

        Args:
            fit_val (float): Fitness value for the calculation run.
            run_id (int): Identifier of the calculation run.
            gb (dict): Global best values.

        Notes:
            This method updates the fitness value and position of the Rosenbrock particle.
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
                print("done for particle with id: ", self.id)
                # update fitness value this particle
                self.current_fitness = self._get_avg_fitness_value()

                # update personal best if applied
                # TODO: make this right in the Webots PSO!!!!!
                if fit_val < self.pb_fitness:
                    self.pb = self.pos
                    self.pb_fitness = fit_val

                # update velocity
                self.pos.vel_x = self._update_variable(self.pos.vel_x, self.pos.x, self.pb.x, gb["x"])
                self.pos.vel_y = self._update_variable(self.pos.vel_y, self.pos.y, self.pb.x, gb["y"])

                # set fitness value to up to date
                self.state = State.SOLVED

    def reset(self):
        """
        Reset the position and state of the Rosenbrock particle.

        Notes:
            This method updates the position, state, and history of the Rosenbrock particle.
        """
        with open("results.json", 'r') as f:
            values = json.load(f)
            # "rw_mean": 7271.369400722904, "rw_variance": 2457.6745646676545, "tao": 1000, "u_plus": 0, "p_c": 1, "report_data": true, "nr_robots": 4}
            print(values)
            values[self.id]["fitness"].append(self.current_fitness)
            values[self.id]["x"].append(self.pos.x)
            values[self.id]["y"].append(self.pos.y)
            values[self.id]["pb"].append(self.pb_fitness)      

        with open("results.json", 'w') as f:
            f.write(json.dumps(values, indent=2))
            f.close()

        self.pos.x += self.pos.vel_x
        self.pos.y += self.pos.vel_y

        # set new value to be not up to date
        self.state = State.UNSOLVED
        self.runs = [ParticleRun(i) for i in range(self.nr_runs)]
