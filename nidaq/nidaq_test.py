"""Example of AI raw operation."""
import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections
import nidaqmx
import time

pp = pprint.PrettyPrinter(indent=4)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    in_stream = task.in_stream

    while time.time() < time.time()+60*5: # 5 mins loop time
    #print("1 Channel 1 Sample Read Raw: ")
         data = in_stream.read(number_of_samples_per_channel=1)
         pp.pprint(data)
         # plot here

    print("1 Channel N Samples Read Raw: ")
    data = in_stream.read(number_of_samples_per_channel=8)
    pp.pprint(data)

    task.ai_channels.add_ai_voltage_chan("Dev1/ai1")

    print("N Channel 1 Sample Read Raw: ")
    data = in_stream.read(number_of_samples_per_channel=1)
    pp.pprint(data)

    print("N Channel N Samples Read Raw: ")
    data = in_stream.read(number_of_samples_per_channel=8)
    pp.pprint(data)
