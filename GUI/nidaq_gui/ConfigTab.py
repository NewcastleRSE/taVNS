import tkinter as tk
from DS8RGlobals import DS8RGlobals
from Globals import Globals


class ConfigTab(tk.Frame):

    def __init__(self, tab_control, global_vars: Globals):
        super().__init__()
        self.global_vars = global_vars
        col1_x = 20
        col1_y = 30
        col2_x = 150
        col2_y = 20
        line_height = 40

        tk.Label(self, text='DS8R stimulation parameters:').place(x=5, y=10, anchor='w')
        xf = tk.Frame(self, relief="groove", borderwidth=2)
        xf.place(x=5, y=10, anchor="nw")
        # STIMULATION PARAMETER WIDGETS
        self.ds8r_mode_label = tk.Label(self, text="Mode:", fg="#0D6519")
        self.s_ds8r_mode = tk.StringVar()
        self.s_ds8r_polarity = tk.StringVar()
        self.s_ds8r_source = tk.StringVar()
        self.s_ds8r_demand = tk.StringVar()
        self.s_ds8r_pulse_width = tk.StringVar()
        self.s_ds8r_dwell = tk.StringVar()
        self.s_ds8r_recovery = tk.StringVar()
        self.s_ds8r_enabled = tk.StringVar()
        self.s_ds8r_mode.set(str(DS8RGlobals.ds8r_mode))
        self.s_ds8r_polarity.set(str(DS8RGlobals.ds8r_polarity))
        self.s_ds8r_source.set(str(DS8RGlobals.ds8r_source))
        self.s_ds8r_demand.set(str(DS8RGlobals.ds8r_demand))
        self.s_ds8r_pulse_width.set(str(DS8RGlobals.ds8r_pulse_width))
        self.s_ds8r_dwell.set(str(DS8RGlobals.ds8r_dwell))
        self.s_ds8r_recovery.set(str(DS8RGlobals.ds8r_recovery))
        self.s_ds8r_enabled.set(str(DS8RGlobals.ds8r_enabled))
        self.ds8r_mode_entry = tk.Entry(self, textvariable=self.s_ds8r_mode, validate="focusout",
                                        validatecommand=lambda:
                                        self.change_colour(self.ds8r_mode_label, self.s_ds8r_mode,
                                                           DS8RGlobals.ds8r_mode, 0))
        self.ds8r_polarity_label = tk.Label(self, text="Polarity:", fg="#0D6519")
        self.ds8r_polarity_entry = tk.Entry(self, textvariable=self.s_ds8r_polarity, validate="focusout",
                                            validatecommand=lambda:
                                            self.change_colour(self.ds8r_polarity_label, self.s_ds8r_polarity,
                                                               DS8RGlobals.ds8r_polarity, 1))
        self.ds8r_source_label = tk.Label(self, text="Source:", fg="#0D6519")
        self.ds8r_source_entry = tk.Entry(self, textvariable=self.s_ds8r_source, validate="focusout",
                                          validatecommand=
                                          lambda: self.change_colour(self.ds8r_mode_label, self.s_ds8r_source,
                                                                     DS8RGlobals.ds8r_source, 2))
        self.ds8r_demand_label = tk.Label(self, text="Demand:", fg="#0D6519")
        self.ds8r_demand_entry = tk.Entry(self, textvariable=self.s_ds8r_demand, validate="focusout",
                                          validatecommand=
                                          lambda: self.change_colour(self.ds8r_demand_label, self.s_ds8r_demand,
                                                                     DS8RGlobals.ds8r_demand, 3))
        self.ds8r_pulse_width_label = tk.Label(self, text="Pulse Width:", fg="#0D6519")
        self.ds8r_pulse_width_entry = tk.Entry(self, textvariable=self.s_ds8r_pulse_width, validate="focusout",
                                               validatecommand=
                                               lambda: self.change_colour(self.ds8r_pulse_width_label,
                                                                          self.s_ds8r_pulse_width,
                                                                          DS8RGlobals.ds8r_pulse_width, 4))
        self.ds8r_dwell_label = tk.Label(self, text="Dwell:", fg="#0D6519")
        self.ds8r_dwell_entry = tk.Entry(self, textvariable=self.s_ds8r_dwell, validate="focusout",
                                         validatecommand=
                                         lambda: self.change_colour(self.ds8r_dwell_label, self.s_ds8r_dwell,
                                                                    DS8RGlobals.ds8r_dwell, 5))
        self.ds8r_recovery_label = tk.Label(self, text="Recovery:", fg="#0D6519")
        self.ds8r_recovery_entry = tk.Entry(self, textvariable=self.s_ds8r_recovery, validate="focusout",
                                            validatecommand=
                                            lambda: self.change_colour(self.ds8r_recovery_label, self.s_ds8r_recovery,
                                                                       DS8RGlobals.ds8r_recovery, 6))
        self.ds8r_enabled_label = tk.Label(self, text="Enabled:", fg="#0D6519")
        self.ds8r_enabled_entry = tk.Entry(self, textvariable=self.s_ds8r_enabled, validate="focusout",
                                           validatecommand=
                                           lambda: self.change_colour(self.ds8r_enabled_label, self.s_ds8r_enabled,
                                                                      DS8RGlobals.ds8r_enabled, 7))
        self.ds8r_mode_label.place(x=col1_x, y=col1_y)
        self.ds8r_mode_entry.place(x=col2_x, y=col2_y)
        self.ds8r_polarity_label.place(x=col1_x, y=col1_y + line_height)
        self.ds8r_polarity_entry.place(x=col2_x, y=col2_y + line_height)
        self.ds8r_source_label.place(x=col1_x, y=col1_y + (line_height * 2))
        self.ds8r_source_entry.place(x=col2_x, y=col2_y + (line_height * 2))
        self.ds8r_demand_label.place(x=col1_x, y=col1_y + (line_height * 3))
        self.ds8r_demand_entry.place(x=col2_x, y=col2_y + (line_height * 3))
        self.ds8r_pulse_width_label.place(x=col1_x, y=col1_y + (line_height * 4))
        self.ds8r_pulse_width_entry.place(x=col2_x, y=col2_y + (line_height * 4))
        self.ds8r_dwell_label.place(x=col1_x, y=col1_y + (line_height * 5))
        self.ds8r_dwell_entry.place(x=col2_x, y=col2_y + (line_height * 5))
        self.ds8r_recovery_label.place(x=col1_x, y=col1_y + (line_height * 6))
        self.ds8r_recovery_entry.place(x=col2_x, y=col2_y + (line_height * 6))
        self.ds8r_enabled_label.place(x=col1_x, y=col1_y + (line_height * 7))
        self.ds8r_enabled_entry.place(x=col2_x, y=col2_y + (line_height * 7))

    def change_colour(self, label, new_value, default, which):
        """
        Change the text colour of *label* to red if *new_value* is different from *default*
        :param label:  the tk.label to be changed
        :param new_value: the new value
        :param default: the default value
        :return: true
        """
        self.update_global(which)
        if new_value.get() == str(default):
            label.config(fg="green")
        else:
            label.config(fg="red")
        return True

    def update_global(self, which):
        match which:
            case 0:
                self.global_vars.mode = int(self.s_ds8r_mode.get())
            case 1:
                self.global_vars.polarity = int(self.s_ds8r_polarity.get())
            case 2:
                self.global_vars.source = int(self.s_ds8r_source.get())
            case 3:
                self.global_vars.demand = int(self.s_ds8r_demand.get())
            case 4:
                self.global_vars.pulse_width = int(self.s_ds8r_pulse_width.get())
            case 5:
                self.global_vars.recovery = int(self.s_ds8r_recovery.get())
            case 6:
                self.global_vars.enabled = int(self.s_ds8r_enabled.get())
            case 7:
                self.global_vars.dwell = int(self.s_ds8r_dwell.get())

