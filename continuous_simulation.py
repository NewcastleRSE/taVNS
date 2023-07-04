import matplotlib.pyplot as plt
from math import sin
import breathingmodel.breathingmodel as b

DELAY = 0.5
FREQUENCY = 10
RESOLUTION = 100

plt.ion()
t = 0
while True:
    x = [t + v * FREQUENCY / RESOLUTION for v in range(RESOLUTION)]
    y = list(map(b.twocomplinear, x))
    print(t,x,y)
    # y = [sin(t + v * 0.1) for v in x]
    # plt.gca().cla() # optionally clear axes
    plt.plot(x, y)
    plt.title(str(t))
    plt.draw()
    plt.pause(DELAY)
    t += 0.5

plt.show(block=True)
