import nidaqmx
import time
from threading import *


class NiDAQ:

    def __init__(self, global_vars):
        self.global_vars = global_vars
        pass

    def record(self):
        with nidaqmx.Task() as task:
            while True:
                if self.global_vars.all_stop:
                    break
                try:
                    task.ai_channels.add_ai_voltage_chan(self.global_vars.device)
                    print("Waiting for nidaq")
                    if self.global_vars.flag_stop:
                        break
                except nidaqmx.errors.DaqError as inst:
                    print("Type:", type(inst))  # the exception type
                    print("Arguments:")  # arguments stored in .args
                    for arg in inst.args:  # unpack args
                        print(arg)
                    continue
                break

            in_stream = task.in_stream
            while not self.global_vars.all_stop:
                print("go")
                while self.global_vars.flag_stop:
                    pass
                    if self.global_vars.all_stop:
                        break
                while not self.global_vars.flag_stop:
                    if self.global_vars.all_stop:
                        break
                    data = in_stream.read(number_of_samples_per_channel=8)
                    data_mean = data.mean()
                    # Update GUI with data value
                    scaled_data = self.global_vars.normalise(data_mean, self.global_vars.plot_min, self.global_vars.plot_max, -100, 100)
                    self.global_vars.belt_value = scaled_data
                    if scaled_data > self.global_vars.belt_max:
                        self.global_vars.belt_max = scaled_data
                        self.global_vars.belt_max = self.global_vars.belt_max
                    if scaled_data < self.global_vars.belt_min:
                        self.global_vars.belt_min = scaled_data
                        self.global_vars.belt_min = self.global_vars.belt_min
                    if scaled_data > self.global_vars.threshold:
                        self.global_vars.stim.run()
                        self.global_vars.stimulating = True
                        self.global_vars.ds8r_stim.append(self.global_vars.threshold)
                    else:
                        self.global_vars.stimulating = False
                        self.global_vars.ds8r_stim.append(0)
                    self.global_vars.x.append(time.time())
                    self.global_vars.y.append(data)
                    self.global_vars.y_mean.append(data_mean)
                if len(self.global_vars.y_mean) > 0:
                    print("max value: ", max(self.global_vars.y_mean))
                    print("min value: ", min(self.global_vars.y_mean))

    def threading(self):
        print("Spawn recording thread ...")
        print("Flag stop: ", self.global_vars.flag_stop)
        t1 = Thread(target=self.record, name="RecordingThread")
        t1.start()
