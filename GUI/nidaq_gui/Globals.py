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
    threshold = 60
    device = "Dev1/ai0"
    x = []
    y = []
    y_mean = []
    ds8r_stim = []
    time_out = 15  # seconds
    flag_stop = True
    belt_max = float("-inf")
    belt_min = float("inf")
    plot_min = -100
    plot_max = 100
    belt_value = 0
    stimulating = False

    def normalise(self, val, min, max, a, b):
        return a + ((val - min) * (b - a)) / (max - min)
