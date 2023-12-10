import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import nidaqmx

fig, ax = plt.subplots(figsize=(6, 3))
x = range(20)
y = [0] * 20

bars = ax.bar(x, y, color="blue")
ax.axis([0, 20, 0, 10])  # x-axis from 0 to 20


# y-axis from 0 to 10

def update(frame):
    data = in_stream.read(number_of_samples_per_channel=1)
    data = data / 1000
    y[frame] = int(data)  # np.random.randint(0, 10)
    bars[frame].set_height(y[frame])


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    in_stream = task.in_stream
    anim = FuncAnimation(fig, update, frames=20, interval=100)
    plt.show()
