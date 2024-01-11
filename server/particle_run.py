

class RunState:
    UNSOLVED = 0
    IN_PROGRESS = 1
    SOLVED = 2

class ParticleRun:
    def __init__(self, id):
        self.id = id
        self.state = RunState.UNSOLVED
        self.answer = None
        self.solved_by = None

    def is_unsolved(self):
        if self.state == RunState.UNSOLVED:
            return True
        return False

    def is_in_progress(self):
        return self.state == RunState.IN_PROGRESS
    
    def is_solved(self):
        return self.state == RunState.SOLVED
    
    def update_fit_value(self, fit_val):
        # check if particle is already solved
        if self.state != RunState.SOLVED:
            self.answer = fit_val
            self.state = RunState.SOLVED
            print("particle run with id ", self.id, " updated with value ", self.answer)

    def set_state_to_in_progress(self):
        self.state = RunState.IN_PROGRESS