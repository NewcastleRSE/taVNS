from ds8r import DS8R


class Stimulator(globals):

    def __init__(self):
        self.globals = globals
        self.initialise()

    def initialise(self):
        globals.stim = DS8R(self.globals.mode, globals.polarity, globals.source, globals.demand,
                            globals.pulse_width, globals.dwell, recovery=globals.recovery,
                            enabled=globals.enabled)
