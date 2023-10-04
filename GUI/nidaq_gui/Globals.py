from ds8r import DS8R
import numpy as np
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
    run_state = False
    all_stop = False
    # Set your DAQ parameters
    sampling_rate = 1000  # Change this to match your actual sampling rate
    samples_per_channel = 8
    cutoff_frequency = 30  # Adjust the cutoff frequency as needed
    # stimulation parameters
    data_point = 0
    date_point_list = []
    stim = DS8R(DS8RGlobals.ds8r_mode, DS8RGlobals.ds8r_polarity, DS8RGlobals.ds8r_source, DS8RGlobals.ds8r_demand,
                DS8RGlobals.ds8r_pulse_width, DS8RGlobals.ds8r_dwell, recovery=DS8RGlobals.ds8r_recovery,
                enabled=DS8RGlobals.ds8r_enabled)
    stimulation_threshold = 60000
    # stimulation ramping parameters:
    ramp_time = (DS8RGlobals.ds8r_pulse_width + DS8RGlobals.ds8r_dwell) * 8  # give roughly 4 pulses before hitting max?
    max_stim_count = 80
    warning_msg = "Everything is Ok!"
    device = "Dev1/ai0"
    recording_time_series = []  # timestamp
    recording_data_series = []  # incoming breathing rate
    recording_data_mean_series = []  # mean of 8 data points
    recording_stimulation_demand = []  # ds8r demand parameter
    recording_stimulation_threshold = []  # stimulation threshold
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
    today = time.time()

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

