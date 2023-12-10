import numpy as np
import nidaqmx
import matplotlib.pyplot as plt

# Set your DAQ parameters
sampling_rate = 2000  # Set the desired sampling rate
duration = 5  # Set the duration of the sine wave in seconds
amplitude = 5.0  # Set the amplitude of the sine wave in volts
frequency = 10.0  # Set the frequency of the sine wave in Hertz

# Generate time values
time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate the sine wave
sine_wave = amplitude * np.sin(2 * np.pi * frequency * time)

# Create a DAQmx task for analog output
with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")

    # Write the sine wave to the analog output channel
    task.write(sine_wave, auto_start=True)

    # Plot the generated sine wave
    plt.plot(time, sine_wave)
    plt.title('Generated Sine Wave')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude (Volts)')
    plt.show()
