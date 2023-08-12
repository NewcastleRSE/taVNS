# https://stackoverflow.com/questions/42192133/embedding-matplotlib-live-plot-data-from-arduino-in-tkinter-canvas

import time
import tkinter as tk
from ds8r import DS8R
import nidaqmx
from threading import *

run_state = False
all_stop = False
# Set your DAQ parameters
sampling_rate = 1000  # Change this to match your actual sampling rate
samples_per_channel = 8
cutoff_frequency = 30  # Adjust the cutoff frequency as needed

stim = DS8R(mode=1, polarity=1, source=1, demand=40,
            pulse_width=500, dwell=10, recovery=40, enabled=1)
threshold = -60
device = "Dev1/ai0"
x = []
y = []
y_mean = []
ds8r_stim = []
time_out = 15  # seconds
flag_stop = True
belt_max = float("-inf")
belt_min = float("inf")

def clear(event):
    global belt_min, belt_max, x, y, y_mean, ds8r_stim
    belt_max = float("-inf")
    belt_min = float("inf")
    max_value["text"] = belt_max
    min_value["text"] = belt_max
    x.clear()
    y.clear()
    y_mean.clear()
    ds8r_stim.clear()


def handle_click(event):
    global flag_stop, threshold, belt_min, belt_max
    if btn_start["text"] == "GO":
        print(s_threshold.get())
        belt_max = float("-inf")
        belt_min = float("inf")
        max_value["text"] = belt_max
        min_value["text"] = belt_max
        print("Start recording")
        threshold = int(s_threshold.get())
        btn_start["text"] = "STOP"
        btn_start["bg"] = "red"
        btn_start["activebackground"] = "red"
        flag_stop = False
    else:
        print("Stop recording ...")
        btn_start["text"] = "GO"
        btn_start["bg"] = "green"
        btn_start["activebackground"] = "green"
        flag_stop = True


def threading():
    print("Spawn recording thread ...")
    print("Flag stop: ", flag_stop)
    t1 = Thread(target=record, name="RecordingThread")
    t1.start()


def record():
    global flag_stop, belt_min, belt_max, all_stop, threshold

    with nidaqmx.Task() as task:
        while True:
            if all_stop:
                break
            try:
                device=device_entry.get()
                task.ai_channels.add_ai_voltage_chan(device)
                print("Waiting for nidaq")
                if flag_stop:
                    break
            except nidaqmx.errors.DaqError as inst:
                print("Type:", type(inst))  # the exception type
                print("Arguments:")  # arguments stored in .args
                for arg in inst.args:  # unpack args
                    print(arg)
                continue
            break

        in_stream = task.in_stream
        end_time = time.time() + time_out
        while not all_stop:
            print("go")
            while flag_stop:
                pass
                if all_stop:
                    break
            while not flag_stop:
                if all_stop:
                    break
                data = in_stream.read(number_of_samples_per_channel=8)
                data_mean = data.mean()
                belt_value["text"] = data_mean
                if data_mean > belt_max:
                    belt_max = data_mean
                    max_value["text"] = belt_max
                if data_mean < belt_min:
                    belt_min = data_mean
                    min_value["text"] = belt_min
                if data_mean > threshold:
                    stim.run()
                    ds8r_stim.append(threshold)
                else:
                    ds8r_stim.append(0)
                x.append(time.time())
                y.append(data)
                y_mean.append(data_mean)
            print("max value: ", max(y_mean))
            print("min value: ", min(y_mean))


def on_closing():
    global flag_stop, all_stop
    flag_stop = True
    all_stop = True
    print("stop")
    window.destroy()
#    raise Exception('Close')


def calibrate():
    pass


window = tk.Tk()
window.geometry("640x480")
window.title("taVNS Controller")

frame1 = tk.Frame(master=window, width=200, height=100, )
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

btn_start = tk.Button(master=window, text="GO", bg="green", activebackground="#0f0")
btn_start.bind("<Button-1>", handle_click)
btn_start.place(x=20, y=20)

btn_clear = tk.Button(master=window, text="Clear", bg="yellow", activebackground="yellow")
btn_clear.bind("<Button-1>", clear)
btn_clear.place(x=60, y=20)

device_label = tk.Label(master=frame1, text="dev#/port")
device_label.place(x=5, y=60)
s_device = tk.StringVar()
device_entry = tk.Entry(master=frame1, textvariable=s_device, )
device_entry.place(x=80, y=60)
s_device.set(device)

threshold_label = tk.Label(master=frame1, text="Threshold:")
threshold_label.place(x=0, y=80)

s_threshold = tk.StringVar()
threshold_entry = tk.Entry(master=frame1, textvariable=s_threshold, )
threshold_entry.place(x=80, y=80)
s_threshold.set(str(threshold))

belt_label = tk.Label(master=frame1, text="Belt in:")
belt_label.place(x=0, y=100)
belt_value = tk.Label(master=frame1, text="")
belt_value.place(x=40, y=100)

max_label = tk.Label(master=frame1, text="Max belt value:")
max_label.place(x=0, y=120)
max_value = tk.Label(master=frame1, text="")
max_value.place(x=100, y=120)

min_label = tk.Label(master=frame1, text="Min belt value:")
min_label.place(x=0, y=140)
min_value = tk.Label(master=frame1, text="")
min_value.place(x=100, y=140)

btn_calibrate = tk.Button(master=window, text="Calibrate")
btn_calibrate.bind("<Button-1>", calibrate)

threading()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
