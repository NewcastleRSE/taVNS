import time
from ds8r.ds8r import DS8R
import nidaqmx
import matplotlib.pyplot as plt

# Set your DAQ parameters
sampling_rate = 1000  # Change this to match your actual sampling rate
samples_per_channel = 8
cutoff_frequency = 30  # Adjust the cutoff frequency as needed

stim = DS8R(mode=1, polarity=1, source=1, demand=40,
            pulse_width=500, dwell=10, recovery=40, enabled=1)
threshhold = 115
x = []
y = []
y_mean = []
ds8rstim = []

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
    # task.ai_dig_fltr_lowpass_cutoff_freq = 1.0
    # task.ai_dig_fltr_enable = True
    # task.timing.cfg_samp_clk_timing(rate=sampling_rate, samps_per_chan=samples_per_channel)
    in_stream = task.in_stream
    end_time = time.time() + 60
    while time.time() < end_time:
        data = in_stream.read(number_of_samples_per_channel=8)
        if data.mean() > threshhold:
            stim.run()
            ds8rstim.append(threshhold)
            #time.sleep(0.2)
        else:
            ds8rstim.append(0)
        x.append(time.time())
        y.append(data)
        y_mean.append(data.mean())


plt.plot(x, y)
plt.show()
plt.plot(x, y_mean)
plt.plot(x, ds8rstim)
plt.show()
