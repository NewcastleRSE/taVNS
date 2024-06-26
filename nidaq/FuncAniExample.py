# https://coderslegacy.com/python/matplotlib-funcanimation/
# https://pythonprogramming.net/embedding-live-matplotlib-graph-tkinter-gui/
# https://stackoverflow.com/questions/457246/what-is-the-best-real-time-plotting-widget-for-wxpython


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')


def init():
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    return ln,


def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,


ani = FuncAnimation(fig, update, frames=60, init_func=init, blit=True)
plt.show()
