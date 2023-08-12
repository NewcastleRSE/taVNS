# https://github.com/WaveShapePlay/Arduino_RealTimePlot/blob/master/Part2_RealTimePlot_UsingClass/ArduinoRealTimePlot.py
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import nidaqmx


class AnimationPlot:

    def animate(self, i, data_list, task):
        data = in_stream.read(number_of_samples_per_channel=1)
        print(data)
        scaled_data = data/10
        print(scaled_data)
        try:
            data_list.append(scaled_data)  # Add to the list holding the fixed number of points to animate
        except:  # Pass if data point is bad
            pass
        data_list = data_list[-100:]  # Fix the list size so that the animation plot 'window' is x number of points
        ax.clear()  # Clear last data frame
        self.get_plot_format()
        ax.plot(data_list)  # Plot new data frame

    def get_plot_format(self):
        ax.set_ylim([100, 1060])  # Set Y axis limit of plot
        ax.set_title("Arduino Data")  # Set title of figure
        ax.set_ylabel("Value")  # Set title of y axis


dataList = []  # Create empty list variable for later use
fig = plt.figure()  # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)  # Add subplot to main fig window
realTimePlot = AnimationPlot()
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    in_stream = task.in_stream
    time.sleep(2)  # Time delay for Arduino Serial initialization
    # Matplotlib Animation Function that takes care of real time plot.
    # Note that 'fargs' parameter is where we pass in our dataList and Serial object.
    ani = animation.FuncAnimation(fig, realTimePlot.animate, frames=100, fargs=(dataList, task), interval=200)
    plt.show()  # Keep Matplotlib plot persistent on screen until it is closed
