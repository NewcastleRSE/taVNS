# https://github.com/ni/nidaqmx-python
# https://github.com/CCS-Lab/DS8R_python
from ds8r import DS8R
import nidaqmx
import time
from threading import *
import logging
from Globals import normalise
import numpy as np

class NiDAQ:

    def __init__(self, global_vars):
        logging.basicConfig(level=logging.INFO)
        self.global_vars = global_vars

    def record(self):
        with nidaqmx.Task() as task:
            while True:
                while True:
                    # break from this thread when window is closed
                    if self.global_vars.all_stop:
                        logging.info('Close thread on window close')
                        break
                    try:
                        logging.info('Check NiDAQ ' + self.global_vars.device + ' availability')
                        self.global_vars.is_nidaq_active = True
                        ai_channel = task.ai_channels.add_ai_voltage_chan(self.global_vars.device)
                        if self.global_vars.flag_stop:
                            break
                    except nidaqmx.errors.DaqError as inst:
                        logging.error("NiDAQ possibly switched off")
                        # print("Type:", type(inst))  # the exception type
                        # print("Arguments:")  # arguments stored in .args
                        # for arg in inst.args:  # unpack args
                        #     print(arg)
                        self.global_vars.is_nidaq_active = False
                        continue
                    # break
                if self.global_vars.all_stop:
                    logging.info('Close thread on window close')
                    break
                in_stream = task.in_stream
                while not self.global_vars.all_stop:
                    while self.global_vars.flag_stop:
                        time.sleep(0.5)
                        if self.global_vars.all_stop:
                            break
                    while not self.global_vars.flag_stop:
                        if self.global_vars.all_stop:
                            break
                        try:
                            data = in_stream.read(number_of_samples_per_channel=8)
                        except nidaqmx.errors.DaqError as inst:
                            self.global_vars.is_nidaq_active = False
                            break
                        data_mean = data.mean()
                        # Update GUI with data value
                        scaled_data = normalise(data_mean, self.global_vars.plot_min, self.global_vars.
                                                                 plot_max, -100, 100)
                        self.global_vars.current_belt_value = scaled_data
                        # set maximum recorded data point
                        if scaled_data > self.global_vars.belt_max:
                            self.global_vars.belt_max = scaled_data
                            self.global_vars.belt_max = self.global_vars.belt_max
                        # set minimum recorded data point
                        if scaled_data < self.global_vars.belt_min:
                            self.global_vars.belt_min = scaled_data
                            self.global_vars.belt_min = self.global_vars.belt_min
                        # if threshold exceeded then stimulate
                        if scaled_data > self.global_vars.stimulation_threshold:
                            self.global_vars.is_stimulating = True
                            self.stim_thread()  # spool up a stimulation thread
                            self.global_vars.recording(data, self.global_vars.stimulation_threshold, 0, data_mean)
                        else:
                            self.global_vars.is_stimulating = False
                            self.global_vars.recording(data, 0, 0, data_mean)

                    if len(self.global_vars.recording_data_mean_series) > 0:
                        print("max value: ", max(self.global_vars.recording_data_mean_series))
                        print("min value: ", min(self.global_vars.recording_data_mean_series))

    def threading(self):
        print("Spawn recording thread ...")
        t1 = Thread(target=self.record, name="RecordingThread")
        t1.start()

    def stimulation(self):
        self.stim_ramp()
        stim_cap = 0
        while self.global_vars.is_stimulating:
            self.global_vars.stim.run()
            self.global_vars.recording(0, self.global_vars.stimulation_threshold, self.global_vars.demand, 0)
            # self.global_vars.recording(0, 0, self.global_vars.demand, 0)
            print("Stim demand: " + self.global_vars.demand)
            stim_cap = stim_cap + 1
            # if we go over the max number of pulses then stop!
            if stim_cap > self.global_vars.max_stim_count:
                self.global_vars.warning_msg("Max stim count reached, the device may need recalibrating.")
                Warning(self.global_vars.warning_msg)
                break
            if self.global_vars.all_stop:
                break

    def stim_thread(self):
        print("Stimulation triggered")
        t2 = Thread(target=self.stimulation, name="Stimulation Thread")
        t2.start()

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
        max_demand = self.global_vars.demand
        pulse_heights = np.linspace(min_demand, self.global_vars.demand, num_ramps)
        print(len(pulse_heights), pulse_heights)
        # create the stimulation profiles for the pulses and run
        for ramp_demand in pulse_heights:
            self.global_vars.demand = ramp_demand
            stim_ramped = DS8R(mode=self.global_vars.mode, polarity=self.global_vars.polarity, source=self.global_vars.source, demand=round(ramp_demand),
                               pulse_width=self.global_vars.pulse_width, dwell=self.global_vars.dwell, recovery=100, enabled=1)
            stim_ramped.run()
            self.global_vars.recording(0, self.global_vars.stimulation_threshold, self.global_vars.demand, 0)
            if not self.global_vars.is_stimulating:
                self.global_vars.demand = max_demand
                break
