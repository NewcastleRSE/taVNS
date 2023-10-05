from threading import *
from Globals import *


class Stimulator:

    def __init__(self, global_vars):
        self.global_vars = global_vars

    def stimulation(self):
        self.stim_ramp()
        stim_cap = 0
        while self.global_vars.is_stimulating:
            self.global_vars.stim.run()
            self.global_vars.recording(0, self.global_vars.stimulation_threshold, self.global_vars.demand, 0)
            # self.global_vars.recording(0, 0, self.global_vars.demand, 0)
            stim_cap = stim_cap + 1
            # if we go over the max number of pulses then stop!
            if stim_cap > self.global_vars.max_stim_count:
                self.global_vars.warning_msg("Max stim count reached, the device may need recalibrating.")
                Warning(self.global_vars.warning_msg)
                break
            if self.global_vars.all_stop:
                break

    def stim_ramp(self):
        # set up and run a set of stimulations that ramp up to max.
        # Once at max will want to switch to just squarewave stims at max
        # calculate the number of pulses needed to reach max during the given ramptime
        num_ramps = round(self.global_vars.ramp_time / ((self.global_vars.pulse_width * 2) + self.global_vars.dwell))
        # calculate the pulse heights in order to have an even gradiated increase in
        # amplitude for each pulse in the ramp
        min_demand = self.global_vars.demand / num_ramps
        if min_demand < 20:
            min_demand = 20
        pulse_heights = np.linspace(min_demand, self.global_vars.demand, num_ramps)
        # create the stimulation profiles for the pulses and run
        for ramp_demand in pulse_heights:
            stim_ramped = DS8R(mode=self.global_vars.mode, polarity=self.global_vars.polarity,
                               source=self.global_vars.source, demand=round(ramp_demand),
                               pulse_width=self.global_vars.pulse_width, dwell=self.global_vars.dwell,
                               recovery=100, enabled=1)
            stim_ramped.run()
            self.global_vars.recording(0, self.global_vars.stimulation_threshold,
                                       round(ramp_demand), self.global_vars.data_point)
            if not self.global_vars.is_stimulating:
                break


    def threading(self):
        t2 = Thread(target=self.stimulation, name="Stimulation Thread")
        t2.start()
