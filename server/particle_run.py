"""
File: particle_run.py
Date: 13-01-24
Description: This script contains the ParticleRun class.
Author: Martijn Schippers
"""

class RunState:
    """
    Enumeration representing the possible states of a ParticleRun instance.

    Attributes:
        UNSOLVED (int): State indicating the run is unsolved.
        IN_PROGRESS (int): State indicating the run is in progress.
        SOLVED (int): State indicating the run is solved.
    """
    UNSOLVED = 0
    IN_PROGRESS = 1
    SOLVED = 2

class ParticleRun:
    """
    The ParticleRun class represents the state and progress of a particle run.

    Attributes:
        id (any): Identifier for the ParticleRun instance.
        state (int): Current state of the run (UNSOLVED, IN_PROGRESS, SOLVED).
        answer (any): Computed fitness value for the run.
        solved_by (any): Identifier of the entity (e.g., PSO particle) that solved the run.
    """

    def __init__(self, id):
        """
        Initialize a ParticleRun instance.

        Args:
            id (any): Identifier for the ParticleRun instance.
        """
        self.id = id
        self.state = RunState.UNSOLVED
        self.answer = None
        self.solved_by = None

    def is_unsolved(self):
        """
        Check if the run is in the UNSOLVED state.

        Returns:
            bool: True if the run is unsolved, False otherwise.
        """
        return self.state == RunState.UNSOLVED

    def is_in_progress(self):
        """
        Check if the run is in the IN_PROGRESS state.

        Returns:
            bool: True if the run is in progress, False otherwise.
        """
        return self.state == RunState.IN_PROGRESS

    def is_solved(self):
        """
        Check if the run is in the SOLVED state.

        Returns:
            bool: True if the run is solved, False otherwise.
        """
        return self.state == RunState.SOLVED

    def update_fit_value(self, fit_val):
        """
        Update the fitness value for the run.

        Args:
            fit_val (any): New fitness value.

        Notes:
            This method sets the run to the SOLVED state and prints a message.
            It does nothing if the run is already in the SOLVED state.
        """
        if self.state != RunState.SOLVED:
            self.answer = fit_val
            self.state = RunState.SOLVED
            print("Particle run with id", self.id, "updated with value", self.answer)

    def set_state_to_in_progress(self):
        """
        Set the state of the run to IN_PROGRESS.

        Notes:
            This method is called when the run transitions to the in-progress state.
        """
        self.state = RunState.IN_PROGRESS
