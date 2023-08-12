class AnimationPlot:

    def __init__(self, global_vars, ax):
        self.ax = ax
        self.global_vars = global_vars

    def animate(self, i, data_list):
        data = self.global_vars.belt_value
        print("Data:", data)
        try:
            data_list.append(data)  # Add to the list holding the fixed number of points to animate
        except:  # Pass if data point is bad
            pass
        data_list = data_list[-100:]  # Fix the list size so that the animation plot 'window' is x number of points
        self.ax.clear()  # Clear last data frame
        self.get_plot_format()
        self.ax.plot(data_list)  # Plot new data frame

    def get_plot_format(self):
        self.ax.set_ylim([-100, 100])  # Set Y axis limit of plot
        self.ax.set_xlim([0, 100])
        self.ax.set_title("Arduino Data")  # Set title of figure
        self.ax.set_ylabel("Value")  # Set title of y axis