import pandas as pd
import matplotlib.pyplot as plt
from Globals import normalise

recording = pd.read_csv('2023-08-21_225053_data.csv', header=None)

data = [float(d) for d in recording.T.iloc[0:, 2]]
stim_demand = [float(d) for d in recording.T.iloc[0:, 3]]
stim_threshold = [float(d) for d in recording.T.iloc[0:, 4]]
time = list(range(0, len(data)))

data_max = max(data)
data_min = min(data)
n_data = [normalise(d, data_min, data_max, -100, 100) for d in data]
n_demand = [normalise(d, data_min, data_max, -100, 100) for d in stim_demand]
n_threshold = [normalise(d, data_min, data_max, -100, 100) for d in stim_threshold]

print(min(stim_demand), max(stim_demand))
plt.plot(time, n_data)
plt.plot(stim_demand, label="Stim demand")
plt.plot(stim_threshold, label="Stim threshold")
plt.show()
