import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import nidaqmx
import time

channel = "Dev1/ai1"
fig, ax = plt.subplots()
global ydata
global xdata
global in_stream
xdata, ydata = [], []
xdata =  np.linspace(0,10,10)
ln, = ax.plot([], [], 'ro')


def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    return ln,


def update(frame):
    global in_stream
    if frame>10:
        ax.set_xlim(0,frame+1)
        xdata.append(frame)
    data = in_stream.read(number_of_samples_per_channel=1)
    ydata.append(data/1000)
    print(data/1000)
    ln.set_data(xdata, ydata)
    return ln,

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(channel)
    in_stream = task.in_stream
    ani = FuncAnimation(fig, update, frames=60, init_func=init, blit=True)
    plt.show()
