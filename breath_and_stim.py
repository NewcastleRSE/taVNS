import time

from ds8r import DS8R
from nclstim import stim_fun

duty_cycle_on = 1
freq = 10
stim = DS8R(mode=2, polarity=1, source=1,demand=20,
              pulse_width=500, dwell=10, recovery=40, enabled=1)

# on trigger:
stim_fun(stim,duty_cyle_on,freq)