from cgitb import enable
import time

from ds8r import DS8R
from nclstim import stim_fun
import breathingmodel.breathingmodel as b
import matplotlib.pyplot as plt
from math import sin
import numpy as np


# stim parameters
duty_cycle_on = 1
freq = 10
stim = DS8R(mode=2, polarity=1, source=1,demand=20,
              pulse_width=500, dwell=10, recovery=40, enabled=1)

oncycle  = 5   # time period where stim can be triggered
offcycle = 10  # rest time with no stimulation
delta_t = 0.1  # time step for breathing simulation


triggertime = []
y_save      = []
ontimes     = []
offtimes    = []

t       = 0  # start from time point zero
y_prev  = 0  # previous y value as zero
delta_y = 0  #  change in y

ontime = time.time() + oncycle
nextcyc = time.time() + oncycle + offcycle
maxtime = time.time() + 60*1 # 5 mins breathing model run

while time.time() < maxtime :
    y = b.twocomplinear(t) # breathing signal!

    if time.time() < ontime:
        stim.enabled=1  # enable stim, we are in an oncycle
        ontimes.append(t)
    elif time.time() > ontime and time.time() < nextcyc:
        stim.enabled=0  # disable stim in this time period
        offtimes.append(t)
    else: # if time is > nextcyc
        ontime = time.time() + oncycle
        nextcyc = time.time() + oncycle + offcycle
        print('cycle complete, assigning new cycle period')

    t += delta_t
    # use y values to provide trigger, when delta_y changes from +ive to -ive? 
    # need to account for noise though, so sliding window? 
    if y<y_prev and delta_y>0: # if our new y is now decreasing,
        # but our old change in y was an increase, then we have crested 
        # the peak and want to trigger stimulation?
        # on trigger:
        stim_fun(stim,duty_cycle_on,freq)
        triggertime.append(t)

    delta_y = y - y_prev   # find the change in y since the last cycle
    y_prev  = y            # reassign to be the most recent y value
    y_save.append(y)


# after the full cycle, plot to check this has worked:
timevals = np.arange(0,t,delta_t)

plt.plot(timevals, y_save)
plt.title('breathing signal')

# convert trigger vals into a vector of zeros with 0.5 when stim is triggered?
triggers = [ 1 if item in np.round(triggertime,2) else 0 for item in np.round(timevals,2) ]
ons      = [ 0.2 if item in np.round(ontimes,2) else 0 for item in np.round(timevals,2) ]
offs     = [ -0.2 if item in np.round(offtimes,2) else 0 for item in np.round(timevals,2) ]

plt.plot(timevals,triggers)
plt.plot(timevals,ons)
plt.plot(timevals,offs)

plt.show()
