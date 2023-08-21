from ds8r import DS8R
import numpy as np

class Globals:
    run_state = False
    all_stop = False
    # Set your DAQ parameters
    sampling_rate = 1000  # Change this to match your actual sampling rate
    samples_per_channel = 8
    cutoff_frequency = 30  # Adjust the cutoff frequency as needed
    # stimulation parameters
    mode = 2
    polarity = 1
    source = 1
    demand = 40
    pulse_width = 500
    dwell = 10 
    # set up the default max stimulation
    stim = DS8R(mode, polarity, source, demand,
                pulse_width, dwell, recovery=100, enabled=1) # currently not providing the option to change recovery time or enabled. 
    stimulation_threshold = 60000
    # stimulation ramping parameters:
    ramp_time = (pulse_width+dwell)*8 # give roughly 4 pulses before hitting max?
    max_stim_count = 80
    warning_msg = "Everything is Ok!"
    device = "Dev1/ai2"
    recording_time_series = []
    recording_data_series = []
    recording_data_mean_series = []
    stimulation_series = []
    time_out = 15  # seconds
    flag_stop = True  # Stop the application
    belt_max = float("-inf")  # display value for belt maximum
    belt_min = float("inf")  # display value for bel minimum
    plot_min = -100  # normalisation minimum
    plot_max = 100  # normalisation maximum
    current_belt_value = 0  # last read value for the belt
    """ True while ds8r is stimulating and false when it is not """
    is_stimulating = False  # whether stimulation is on or not
    # True when the nidaq is switched on and false when detected to be off
    is_nidaq_active = False  # whether the nidaq is switched on or not

    def normalise(self, val, min, max, a, b):
        return a + ((val - min) * (b - a)) / (max - min)
    
    def stim_ramp(self):
         # set up and run a set of stimulations that ramp up to max. 
         # Once at max will want to switch to just squarewave stims at max
        num_ramps = self.ramp_time/((self.pulse_width*2)+self.dwell) # calculate the number of pulses needed to reach max during the given ramptime
        pulse_heights = np.linspace(self.demand/num_ramps,self.demand,num_ramps)# calculate the pulse heights in order to have an even gradiated increase in amplitude for each pulse in the ramp
        # create the stimulation profiles for the pulses and run
        for ramp_demand in pulse_heights:
            stim_ramped = DS8R(mode=self.mode, polarity=self.polarity, source=self.source, demand=round(ramp_demand),
                pulse_width=self.pulse_width, dwell=self.dwell, recovery=100, enabled=1 )
            stim_ramped.run()
            if not self.is_stimulating:
                break
