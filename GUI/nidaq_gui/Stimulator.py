from ds8r import DS8R
from Globals import Globals


class Stimulator:
    """
    Interface for stimulator
    """
    def __init__(self, global_vars: Globals):
        self.global_vars = global_vars
        self.initialise()

    def initialise(self):
        """
        Initialise the stimulator
        :return:
        """
        self.global_vars.stim = DS8R(self.global_vars.mode, self.global_vars.polarity, self.global_vars.source,
                                     self.global_vars.demand,
                                     self.global_vars.pulse_width, self.global_vars.dwell,
                                     recovery=self.global_vars.recovery,
                                     enabled=self.global_vars.enabled)
