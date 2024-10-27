from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

# Define the app UI
app_ui = ui.page_fluid(
    ui.h2("Square Function Visualization"),
    ui.input_slider("x_value", "Choose a value for x:", min=0, max=10, value=5),
    ui.output_plot("plot")
)

# Define the server logic
def server(input, output, session):
    @output
    @render.plot
    def plot():
        # Get the current value of x from the slider
        x = input.x_value()
        # Compute y as the square of x
        y = x ** 2
        # Plot the function
        x_vals = np.linspace(0, 10, 100)
        y_vals = x_vals ** 2
        plt.figure()
        plt.plot(x_vals, y_vals, label="y = x^2", color="blue")
        plt.scatter([x], [y], color="red")  # Plot the selected point
        plt.title(f"y = x^2, where x = {x} and y = {y}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

# Create the app instance
app = App(app_ui, server)
