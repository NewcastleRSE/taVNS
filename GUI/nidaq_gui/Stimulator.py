from Globals import Globals


class Stimulator:
    """
    Interface for stimulator
    """
    def __init__(self, global_vars: Globals):
        self.global_vars = global_vars
        self.initialise()

    def initialise(self):
        pass

