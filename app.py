# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive

# Generate a simple dataset
data = pd.DataFrame({
    "Month": pd.date_range(start="2023-01-01", periods=12, freq="M"),
    "Sales": np.random.randint(20, 100, size=12)
})

# Define the Shiny UI
app_ui = ui.page_fluid(
    ui.h2("Monthly Sales Data Plot"),
    
    # Dropdown for selecting a specific month
    ui.input_select("month", "Select Month:", ["All"] + list(data["Month"].dt.strftime("%B"))),
    
    # Output plot
    ui.output_plot("sales_plot")
)

# Define the server logic
def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        # Filter data based on the selected month
        df = data.copy()
        if input.month() != "All":
            df = df[df["Month"].dt.strftime("%B") == input.month()]
        return df

    @output
    @render.plot
    def sales_plot():
        # Generate a line plot of the filtered data
        df = filtered_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df["Month"], df["Sales"], marker='o')
        ax.set_title(f"Sales Data for {input.month() if input.month() != 'All' else 'All Months'}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")
        plt.xticks(rotation=45)
        return fig

# Create the Shiny app
app = App(app_ui, server)
