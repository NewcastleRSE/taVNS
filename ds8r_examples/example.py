import time

from ds8r.ds8r import DS8R

'''
Stimulation Parameters:

 mode is stimulus mode
 Two options, 1=monophasic, 2=biphasic

 polarity is whether the pulses are 
 1 = positive, 
 2 = negative
  or 3 = alternating

 Source, is this the voltage source?

 Demand, a demand of 20 is 2mA

 pulse width, range 50-2000, seems to be in microseconds. 
 (1000micros = 1ms)

 dwell, the time between positive and negative phases when
  in bisphasic mode. Range from 1-990 microseconds,
  so I would guess the units here are microseconds?

 recovery, the amplitude of the recovery phase
  (the negative pulse in  a biphasic pulse)
 this is a percentage of the stimulus phase, 
 so 100% is identical to the stim phase in duration and amplitude
 if you were to set it to 10% it would be 10% of the stimulus amplitude,
 but it would be 10x longer in duration to preserve charge balance.
'''

level5 = DS8R(mode=1, polarity=3, source=1,demand=20,
              pulse_width=1000, dwell=10, recovery=100, enabled=1)
level4 = DS8R(demand=30, pulse_width=900)
level3 = DS8R(demand=20, pulse_width=800)
level2 = DS8R(demand=30, pulse_width=700)
level1 = DS8R(demand=20, pulse_width=600)

level5.run()
time.sleep(1)

level5.run()
time.sleep(1)

level4.run()
time.sleep(1)

level3.run()
time.sleep(1)

level2.run()
time.sleep(1)

level1.run()
