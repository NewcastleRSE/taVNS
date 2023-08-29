from datetime import datetime
import csv
from Globals import *
from Stimulator import *
import time

def save(global_vars):
    """
    Save recording arrays to csv file
    :param event:
    :return:
    """
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d_%H%M%S")
    print(formatted)
    with open(formatted + "_data.csv", 'w') as f:
        write = csv.writer(f)
        write.writerow(global_vars.recording_time_series)
        write.writerow(global_vars.recording_data_series)
        write.writerow(global_vars.recording_data_mean_series)
        write.writerow(global_vars.recording_stimulation_demand)
        write.writerow(global_vars.recording_stimulation_threshold)


global_vars = Globals()
stimulator = Stimulator(global_vars)
stimulator.threading()

try:
    while True:
        global_vars.is_stimulating = True
        print("Stim")
        time.sleep(10)
        global_vars.is_stimulating = False
        print("sleep")
        time.sleep(10)
except KeyboardInterrupt:
    save(global_vars)
    exit(0)


