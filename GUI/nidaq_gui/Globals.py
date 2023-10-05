from ds8r import DS8R
import time
from DS8RGlobals import DS8RGlobals


def normalise(val, data_min, data_max, range_min, range_max):
    """
    normalise value within a specified range
    :param val: the value to be normalised
    :param data_min: the minimum value of the data series
    :param data_max: the maximum value of the data series
    :param range_min: the maximum range value
    :param range_max: the minimum range value
    :return: the normalised value
    """
    return range_min + ((val - data_min) * (range_max - range_min)) / (data_max - data_min)


class Globals:

    def __init__(self):
        self.run_state = False
        self.all_stop = False
        # Set your DAQ parameters
        self.sampling_rate = 1000  # Change this to match your actual sampling rate
        self.samples_per_channel = 8
        self.cutoff_frequency = 30  # Adjust the cutoff frequency as needed
        # stimulation parameters
        self.data_point = 0
        self.date_point_list = []
        self.mode = DS8RGlobals.ds8r_mode
        self.polarity = DS8RGlobals.ds8r_polarity
        self.source = DS8RGlobals.ds8r_source
        self.demand = DS8RGlobals.ds8r_demand
        self.recovery = DS8RGlobals.ds8r_recovery
        self.enabled = DS8RGlobals.ds8r_enabled
        self.dwell = DS8RGlobals.ds8r_dwell
        self.stim = DS8R(DS8RGlobals.ds8r_mode, DS8RGlobals.ds8r_polarity, DS8RGlobals.ds8r_source,
                         DS8RGlobals.ds8r_demand,
                         DS8RGlobals.ds8r_pulse_width, DS8RGlobals.ds8r_dwell, recovery=DS8RGlobals.ds8r_recovery,
                         enabled=DS8RGlobals.ds8r_enabled)
        self.stimulation_threshold = 60000
        # stimulation ramping parameters:
        self.ramp_time = (
                                     DS8RGlobals.ds8r_pulse_width + DS8RGlobals.ds8r_dwell) * 8  # give roughly 4 pulses before hitting max?
        self.pulse_width = DS8RGlobals.ds8r_pulse_width
        self.max_stim_count = 80
        self.warning_msg = "Everything is Ok!"
        self.device = "Dev1/ai0"
        self.recording_time_series = []  # timestamp
        self.recording_data_series = []  # incoming breathing rate
        self.recording_data_mean_series = []  # mean of 8 data points
        self.recording_stimulation_demand = []  # ds8r demand parameter
        self.recording_stimulation_threshold = []  # stimulation threshold
        self.time_out = 15  # seconds
        self.flag_stop = True  # Stop the application
        self.belt_max = float("-inf")  # display value for belt maximum
        self.belt_min = float("inf")  # display value for bel minimum
        self.plot_min = -100  # normalisation minimum
        self.plot_max = 100  # normalisation maximum
        self.current_belt_value = 0  # last read value for the belt
        """ True while ds8r is stimulating and false when it is not """
        self.is_stimulating = False  # whether stimulation is on or not
        # True when the nidaq is switched on and false when detected to be off
        self.is_nidaq_active = False  # whether the nidaq is switched on or not
        self.today = time.time()

    def recording(self, data, stimulation_threshold, stimulation_demand, data_mean):
        """
        Record data in list
        :param data: Currently measured data points
        :param stimulation_threshold: Threshold at which stimulation is applied
        :param stimulation_demand: The demand (current) applied during stimulation)
        :param data_mean: The mean of the measured data points to produce one data point
        :return:
        """
        self.recording_time_series.append(time.time() - self.today)
        self.recording_data_series.append(data)
        self.recording_data_mean_series.append(data_mean)
        self.recording_stimulation_demand.append(stimulation_demand)
        self.recording_stimulation_threshold.append(stimulation_threshold)
