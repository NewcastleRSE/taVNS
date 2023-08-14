from ds8r import DS8R


class Globals:
    run_state = False
    all_stop = False
    # Set your DAQ parameters
    sampling_rate = 1000  # Change this to match your actual sampling rate
    samples_per_channel = 8
    cutoff_frequency = 30  # Adjust the cutoff frequency as needed

    stim = DS8R(mode=1, polarity=1, source=1, demand=40,
                pulse_width=500, dwell=10, recovery=40, enabled=1)
    stimulation_threshold = 60000
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
