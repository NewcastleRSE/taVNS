import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from ConfigTab import ConfigTab
from MainTab import MainTab


class GUI:
    window = tk.Tk()
    main_tab = None

    def __init__(self, global_vars, daq_recorder):
        self.global_vars = global_vars
        tab_control = ttk.Notebook(self.window)
        self.main_tab = MainTab(tab_control, global_vars, daq_recorder)
        config_tab = ConfigTab(tab_control)
        tab_control.add(self.main_tab, text='Main')
        tab_control.add(config_tab, text='DS8R')
        tab_control.pack(expand=1, fill="both")
        self.create_gui()

    def create_gui(self):
        print("Creating GUI")
        self.window.geometry("1024x768")
        self.window.title("taVNS Controller")

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        """ Closing actions:
        When the main window is closed, make sure all threads are stopped by setting the appropriate flags monitored
        by the threads for breaking out.
        """
        answer = tk.messagebox.askyesno("Question", "Would you like to save before exiting?")
        if answer:
            self.main_tab.save(None)
        self.global_vars.flag_stop = True
        self.global_vars.all_stop = True
        print("stop")
        self.window.destroy()
