#!/usr/bin/python
#
# Read stream of lines from an Arduino with a magnetic sensor. This
# produces 3 values per line every 50ms that relate to the orientation
# of the sensor. Each line looks like:
# MAG   1.00    -2.00   0.00
# with each data line starting with "MAG" and each field separated by
# tab characters. Values are floating point numbers in ASCII encoding.
#
# This script supports both Python 2.7 and Python 3

from __future__ import print_function, division, absolute_import
import sys

if sys.hexversion > 0x02ffffff:
    import tkinter as tk
else:
    import Tkinter as tk
import nidaqmx


class App(tk.Frame):

    def __init__(self, parent, title, nidaq):
        tk.Frame.__init__(self, parent)
        self.nidaq = nidaq
        self.npoints = 100
        self.Line1 = [0 for x in range(self.npoints)]
        parent.wm_title(title)
        parent.wm_geometry("800x400")
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.create_line((0, 0, 0, 0), tag='nidaq', fill='darkred', width=1)
        self.canvas.grid(sticky="news")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="news")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def on_resize(self, event):
        self.replot()

    def read_nidaq(self):
        """
        Check for input from the serial port. On fetching a line, parse
        the sensor values and append to the stored data and post a replot
        request.
        """
        data = self.nidaq.read(number_of_samples_per_channel=1) / 100.0
        print(data)
        self.append_values(data)
        self.after_idle(self.replot)
        self.after(10, self.read_nidaq)

    def append_values(self, data):
        """
        Update the cached data lists with new sensor values.
        """
        self.Line1.append(data)
        self.Line1 = self.Line1[-1 * self.npoints:]
        return

    def replot(self):
        """
        Update the canvas graph lines from the cached data lists.
        The lines are scaled to match the canvas size as the window may
        be resized by the user.
        """
        w = self.winfo_width()
        h = self.winfo_height()
        max_all = 2.0
        coordsX = []
        for n in range(0, self.npoints):
            x = (w * n) / self.npoints
            coordsX.append(x)
            coordsX.append(h - ((h * (self.Line1[n] + 100)) / max_all))
        self.canvas.coords('X', *coordsX)


def main(args=None):
    root = tk.Tk()
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        in_stream = task.in_stream
        app = App(root, "NiDAQ Display Dev1/ai0", in_stream)
        app.read_nidaq()
        app.mainloop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
