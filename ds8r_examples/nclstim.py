# A module file to use for our custom ds8r_examples functions
# for the closeNIT taVNS project.
# FT and JS 2023
import time


def stim_fun(stim, duty_cyle_on=1, freq=10):
    '''
    A simple stimulation function, 
    will run for a set on time (duty_cycle_on) in seconds
    with a frequency in Hz and with a stim profile set by 'stim'
    '''
    trest = 1/freq
    oncyc_end = time.time() + duty_cyle_on
    while time.time() < oncyc_end:
        stim.run()
        time.sleep(trest)



# add a function for parsing the input from the breathing belt?

# add function for finding the change in delta y windowed?

# add a function for gathering the GUI inputs?