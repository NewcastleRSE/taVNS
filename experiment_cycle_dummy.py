import matplotlib.pyplot as plt
from nclstim import stim_fun_dummy, DS8R_dummy
import numpy as np


# For taVNS Tiago asked for 100-300ms pulse width, 5-20Hz, 2-20ma
# from literature, "pulse width: 250–500 μs, frequency: 10–25 Hz)
#  and delivered at an individualized constant current (<5 mA)"
# going with biphasic as this seems to be recommended in literature?

# mode is stimulus mode
# Two options, 1=monophasic, 2=biphasic

# polarity is whether the pulses are 
# 1 = positive, 
# 2 = negative
#  or 3 = alternating

# Source, is this the voltage source?

# Demand, a demand of 20 is 2mA

# pulse width, range 50-2000, seems to be in microseconds. 
# (1000micros = 1ms)

# dwell, the time between positive and negative phases when
#  in bisphasic mode. Range from 1-990 microseconds,
#  so I would guess the units here are microseconds?

# recovery, the amplitude of the recovery phase
#  (the negative pulse in  a biphasic pulse)
# this is a percentage of the stimulus phase, 
# so 100% is identical to the stim phase in duration and amplitude
# if you were to set it to 10% it would be 10% of the stimulus amplitude,
# but it would be 10x longer in duration to preserve charge balance.



duty_cyle_on    = 10    # seconds
duty_cycle_off  = 20
experiment_time = 20     # minutes
freq            = 10    # Hz, cycles per second
# Typical duty cycles have 30–60 s "on" periods and 
# 60–120 s "off" periods, or 20–50% duty cycles.


## Set up stimulation protocol for single pulse
# loop for duty_cycle number of seconds
stim = DS8R_dummy(mode=1, polarity=1, source=1, demand=20,
              pulse_width=200, dwell=10, recovery=100, enabled=1)


## loop for the number of iterations needed to meet the duty cycle.
# NB: time this to make sure it is working right

experiment_end = 60*experiment_time  # end experiment 5 mins from now

t = 0
tstep = 0.01
stimall = []
while t < experiment_end:
    print('On cycle')
    stimout,t = stim_fun_dummy(stim, duty_cyle_on, freq,t)
    stimall.extend(stimout)
    print('Off cycle')
    t = t + duty_cycle_off
    stimall.extend([0]*duty_cycle_off)
print('Experiment ended')

# after the full cycle, plot to check this has worked:
timevals = np.arange(0,t)

plt.plot(stimall)
plt.title('stimulation')

plt.show()
