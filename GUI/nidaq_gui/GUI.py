import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from AnimationPlot import AnimationPlot


class GUI:
    window = tk.Tk()
    frame1 = tk.Frame(master=window, width=200, height=100, )
    btn_start = tk.Button(master=window, text="GO", bg="green", activebackground="#0f0")
    btn_clear = tk.Button(master=window, text="Clear", bg="yellow", activebackground="yellow")
    btn_calibrate = tk.Button(master=window, text="Calibrate")
    device_label = tk.Label(master=frame1, text="dev#/port")
    belt_value = tk.Label(master=frame1, text="")
    s_device = tk.StringVar()
    device_entry = tk.Entry(master=frame1, textvariable=s_device, )
    threshold_label = tk.Label(master=frame1, text="Threshold:")
    s_threshold = tk.StringVar()
    threshold_entry = tk.Entry(master=frame1, textvariable=s_threshold, )
    belt_label = tk.Label(master=frame1, text="Belt in:")
    max_label = tk.Label(master=frame1, text="Max belt value:")
    max_value = tk.Label(master=frame1, text="")
    min_label = tk.Label(master=frame1, text="Min belt value:")
    min_value = tk.Label(master=frame1, text="")
    stim_label = tk.Label(master=frame1, text="No Stim", background="#0f0")
    data_list = []

    def __init__(self, global_vars, daq_recorder):
        self.canvas = None
        self.figure = None
        self.ani = None
        self.global_vars = global_vars
        self.daq_recorder = daq_recorder
        self.create_gui()

    def matplotlib_graph(self):
        ax = self.figure.add_subplot(111)
        realtime_plot = AnimationPlot(self.global_vars, ax)
        realtime_plot.get_plot_format()
        self.ani = animation.FuncAnimation(self.figure, realtime_plot.animate, frames=100,
                                           fargs=[self.data_list, ], interval=200)

    def create_gui(self):
        print("Creating GUI")
        self.window.geometry("1024x768")
        self.window.title("taVNS Controller")

        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.btn_start.bind("<Button-1>", self.handle_click)
        self.btn_start.place(x=20, y=20)

        self.btn_clear.bind("<Button-1>", self.clear)
        self.btn_clear.place(x=80, y=20)

        self.btn_calibrate.bind("<Button-1>", self.calibrate)
        self.btn_calibrate.place(x=140, y=20)

        self.stim_label.place(x=220, y=20)

        self.device_label.place(x=5, y=60)
        self.device_entry.place(x=80, y=60)
        self.s_device.set(self.global_vars.device)

        self.threshold_label.place(x=0, y=80)

        self.threshold_entry.place(x=80, y=80)
        self.s_threshold.set(str(self.global_vars.threshold))

        self.belt_label.place(x=0, y=100)
        self.belt_value.place(x=40, y=100)

        self.max_label.place(x=0, y=120)
        self.max_value.place(x=100, y=120)

        self.min_label.place(x=0, y=140)
        self.min_value.place(x=100, y=140)

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure)
        self.canvas.get_tk_widget().place(x=0, y=160)

        self.daq_recorder.threading()

        self.matplotlib_graph()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.after(500, self.update)
        self.window.mainloop()

    def update(self):
        self.max_value["text"] = self.global_vars.belt_max
        self.min_value["text"] = self.global_vars.belt_min
        self.belt_value["text"] = self.global_vars.belt_value
        self.window.after(500, self.update)
        if self.global_vars.stimulating:
            self.stim_label["background"] = "#f00"
        else:
            self.stim_label["background"] = "#0f0"

    def handle_click(self, event):
        self.global_vars.device = self.device_entry.get()
        if self.btn_start["text"] == "GO":
            print(self.s_threshold.get())
            self.global_vars.belt_max = float("-inf")
            self.global_vars.belt_min = float("inf")
            self.max_value["text"] = self.global_vars.belt_max
            self.min_value["text"] = self.global_vars.belt_min
            print("Start recording")
            self.global_vars.threshold = float(self.s_threshold.get())
            self.btn_start["text"] = "STOP"
            self.btn_start["bg"] = "red"
            self.btn_start["activebackground"] = "red"
            self.global_vars.flag_stop = False
        else:
            print("Stop recording ...")
            self.btn_start["text"] = "GO"
            self.btn_start["bg"] = "green"
            self.btn_start["activebackground"] = "green"
            self.global_vars.flag_stop = True

    def clear(self, event):
        self.global_vars.belt_max = float("-inf")
        self.global_vars.belt_min = float("inf")
        self.max_value["text"] = self.global_vars.belt_max
        self.min_value["text"] = self.global_vars.belt_max
        self.global_vars.x.clear()
        self.global_vars.y.clear()
        self.global_vars.y_mean.clear()
        self.global_vars.ds8r_stim.clear()

    def calibrate(self, event):
        self.global_vars.plot_min = self.global_vars.belt_min
        self.global_vars.plot_max = self.global_vars.belt_max

    def on_closing(self):
        self.global_vars.flag_stop = True
        self.global_vars.all_stop = True
        print("stop")
        self.window.destroy()
