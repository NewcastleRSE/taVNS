import nidaqmx
from nidaqmx import constants

# Define the pulse parameters
pulse_duration = 5.0  # in seconds
output_channel = "Dev1/port1/line0"  # Assuming PF1.0 corresponds to the first line of port0

# Create a task
with nidaqmx.Task() as task:
    # Configure the digital output channel
    task.do_channels.add_do_chan(output_channel, line_grouping=constants.LineGrouping.CHAN_PER_LINE)

    # Write a high voltage level (5V) for the specified duration to generate a pulse
    task.write(True, timeout=10.0)

    # Wait for the specified pulse duration
    task.wait_until_done()
    task.write(False, timeout=10.0)

    # The task automatically closes when exiting the 'with' block
