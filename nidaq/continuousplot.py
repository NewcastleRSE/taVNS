import math
from matplotlib import pyplot as plt
import threading
import time


class ContinuousPlot(object):
    def __init__(self, get_data, delay_millis=1000, ax=None):
        self.get_data = get_data
        self.delay = delay_millis / 1000
        self.ax = ax if ax is not None else plt.subplots()[1]

        self.thread = None
        self.is_running = False

    def begin(self):
        self.is_running = True
        self.mainloop()

    def begin_threaded(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.mainloop)
        self.thread.start()

    def end(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()

    def mainloop(self):
        while self.is_running:
            self.tick()
            time.sleep(self.delay)

    def tick(self):
        data = self.get_data()
        if not isinstance(data, list):
            return

        if not all(isinstance(el, list) for el in data):  # Single (non-nested) list
            self.ax.plot(data)
        else:  # nested list
            for line in data:
                self.ax.plot(line)

        plt.show()


def sin_wave(x, frequency, amplitude, offset):
    return math.sin(x * frequency) * amplitude + offset


def example_get_data():
    resolution = 200

    data = []
    params = [(1.0, 1.0, 0.0), (2.0, 0.5, 0.0), (0.2, 0.1, 1.0)]
    t = time.time()
    for p in params:
        data.append([sin_wave(t + i, p[0], p[1], p[2]) for i in range(resolution)])
    return data


if __name__ == "__main__":
    plot = ContinuousPlot(example_get_data, 500)
    plot.begin()
