import csv
from datetime import datetime
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from AnimationPlot import AnimationPlot


def save():
    print("You have to save")


class MainTab(tk.Frame):

    def __init__(self, tab_control, global_vars, daq, config_tab):
        super().__init__()
        self.canvas = None
        self.figure = None
        self.ani = None
        self.global_vars = global_vars
        self.daq = daq
        self.config_tab = config_tab
        default_button_width = 7
        default_button_height = 1
        frame1 = tk.Frame(master=self, width=200, height=100, )
        self.btn_start = tk.Button(master=frame1, text="START RECORDING", bg="green", activebackground="#0f0",
                                   width=15,
                                   height=default_button_height)
        self.btn_clear = tk.Button(master=frame1, text="Clear", bg="yellow", activebackground="yellow",
                                   width=default_button_width, height=default_button_height)
        self.btn_calibrate = tk.Button(master=frame1, text="Calibrate", width=default_button_width,
                                       height=default_button_height)
        self.btn_save = tk.Button(master=frame1, text="Save", width=default_button_width, height=default_button_height)
        self.device_label = tk.Label(master=frame1, text="Dev#/ai#")
        self.belt_value = tk.Label(master=frame1, text="")
        self.s_device = tk.StringVar()
        self.device_entry = tk.Entry(master=frame1, textvariable=self.s_device, )
        self.threshold_label = tk.Label(master=frame1, text="Threshold:")
        self.s_threshold = tk.StringVar()
        self.threshold_entry = tk.Entry(master=frame1, textvariable=self.s_threshold, )
        self.belt_label = tk.Label(master=frame1, text="Belt in (norm):")
        self.max_label = tk.Label(master=frame1, text="Max belt value:")
        self.max_value = tk.Label(master=frame1, text="")
        self.min_label = tk.Label(master=frame1, text="Min belt value:")
        self.min_value = tk.Label(master=frame1, text="")
        self.stim_label = tk.Label(master=frame1, text="No Stim", background="#0f0", height=default_button_height,
                                   width=default_button_width)
        self.nidaq_status_label = tk.Label(master=frame1, text="niDAQ status", background="#f00",
                                           height=default_button_height)
        self.data_list = [[], []]
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.btn_start.bind("<Button-1>", self.go_stop_button)
        self.btn_start.place(x=20, y=20)

        self.btn_clear.bind("<Button-1>", self.clear)
        self.btn_clear.place(x=140, y=20)

        self.btn_calibrate.bind("<Button-1>", self.calibrate)
        self.btn_calibrate.place(x=200, y=20)

        self.btn_save.bind("<Button-1>", self.save)
        self.btn_save.place(x=260, y=20)

        self.stim_label.place(x=360, y=20)

        self.nidaq_status_label.place(x=420, y=20)

        self.device_label.place(x=0, y=60)
        self.device_entry.place(x=80, y=60)
        self.s_device.set(self.global_vars.device)

        self.threshold_label.place(x=0, y=80)

        self.threshold_entry.place(x=80, y=80)
        self.s_threshold.set(str(self.global_vars.stimulation_threshold))

        self.belt_label.place(x=0, y=100)
        self.belt_value.place(x=100, y=100)

        self.max_label.place(x=0, y=120)
        self.max_value.place(x=100, y=120)

        self.min_label.place(x=0, y=140)
        self.min_value.place(x=100, y=140)

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().place(x=0, y=160)

        self.daq.threading()

        self.matplotlib_graph()
        self.update_vars()

    def entries_state(self, state):
        self.config_tab.ds8r_mode_entry.config(state=state)
        self.config_tab.ds8r_polarity_entry.config(state=state)
        self.config_tab.ds8r_source_entry.config(state=state)
        self.config_tab.ds8r_demand_entry.config(state=state)
        self.config_tab.ds8r_pulse_width_entry.config(state=state)
        self.config_tab.ds8r_dwell_entry.config(state=state)
        self.config_tab.ds8r_recovery_entry.config(state=state)
        self.config_tab.ds8r_enabled_entry.config(state=state)

    def update_vars(self):
        self.max_value["text"] = self.global_vars.belt_max
        self.min_value["text"] = self.global_vars.belt_min
        self.belt_value["text"] = self.global_vars.current_belt_value
        self.after(500, self.update_vars)
        if self.global_vars.is_stimulating:
            self.stim_label["background"] = "#f00"
            self.stim_label["text"] = "Stim"
        else:
            self.stim_label["background"] = "#0f0"
            self.stim_label["text"] = "No Stim"
        if self.global_vars.is_nidaq_active:
            self.nidaq_status_label["background"] = "#0f0"
        else:
            self.nidaq_status_label["background"] = "#f00"

    def go_stop_button(self, event):
        """
        Toggle switch to start and stop recording
        :param event:
        :return:
        """
        print(event)
        if self.btn_start["text"] == "START RECORDING":
            print("Start recording ...")
            self.entries_state(tk.DISABLED)
            self.global_vars.device = self.s_device.get()
            self.global_vars.stimulation_threshold = float(self.s_threshold.get())
            self.btn_start["text"] = "STOP RECORDING"
            self.btn_start["bg"] = "red"
            self.btn_start["activebackground"] = "red"
            self.global_vars.flag_stop = False
        else:
            print("Stop recording ...")
            self.entries_state(tk.NORMAL)
            self.btn_start["text"] = "START RECORDING"
            self.btn_start["bg"] = "green"
            self.btn_start["activebackground"] = "green"
            self.global_vars.flag_stop = True

    def clear(self, event):
        """Clear parameters: When the clear button is pressed, clear the parameters used for recording and displaying
        the graph.
        """
        self.global_vars.belt_max = float("-inf")
        self.global_vars.belt_min = float("inf")
        self.max_value["text"] = self.global_vars.belt_max
        self.min_value["text"] = self.global_vars.belt_min
        self.global_vars.recording_time_series.clear()
        self.global_vars.recording_data_series.clear()
        self.global_vars.recording_data_mean_series.clear()
        self.global_vars.recording_stimulation_threshold.clear()
        self.global_vars.recording_stimulation_demand.clear()

    def calibrate(self, event):
        """
        Normalise graph axes. Set normalisation minimum and maximum values based on actual measured maximum and
        minimum values.
        """
        if self.global_vars.belt_max != float("-Inf"):
            self.global_vars.plot_min = self.global_vars.belt_min
            self.global_vars.plot_max = self.global_vars.belt_max
        else:
            self.global_vars.plot_min = -100
            self.global_vars.plot_max = 100

        print("calib", self.global_vars.plot_min)
        print("calib", self.global_vars.plot_max)

    def matplotlib_graph(self):
        ax = self.figure.add_subplot(111)
        realtime_plot = AnimationPlot(self.global_vars, ax)
        realtime_plot.get_plot_format()
        self.ani = animation.FuncAnimation(self.figure, realtime_plot.animate, frames=100,
                                           fargs=[self.data_list, ], interval=200)

    def save(self, event):
        """
        Save recording arrays to csv file
        :param self:
        :param event:
        :return:
        """
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d_%H%M%S")
        print(formatted)
        with open(formatted + "_data.csv", 'w') as f:
            write = csv.writer(f)
            write.writerow(self.global_vars.recording_time_series)
            write.writerow(self.global_vars.recording_data_series)
            write.writerow(self.global_vars.recording_data_mean_series)
            write.writerow(self.global_vars.recording_stimulation_demand)
            write.writerow(self.global_vars.recording_stimulation_threshold)
