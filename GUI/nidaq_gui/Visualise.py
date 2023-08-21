import pandas as pd
import matplotlib.pyplot as plt

recording = pd.read_csv('2023-08-21_141209_data.csv', header=None)

# time = data.T.iloc[0:10000, 0]
data = [float(d) for d in recording.T.iloc[0:, 2]]
stim = [float(d) for d in recording.T.iloc[0:, 4]]
time = list(range(0, len(data)))

print(len(time))
print(len(data))

plt.plot(time, data)
plt.plot(stim, label="Stim")
plt.show()


def normalise(data, min, max):
    pass