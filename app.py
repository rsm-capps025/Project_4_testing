from shiny import App, ui, render
import pandas as pd

# Sample data
data = pd.DataFrame({
    "Car Make": ["Toyota", "Toyota", "Ford", "Ford", "Honda", "Honda", "Chevrolet", "Chevrolet"],
    "Model": ["Camry", "Corolla", "Focus", "Fiesta", "Civic", "Accord", "Malibu", "Impala"],
    "Fuel Type": ["Gasoline", "Diesel", "Gasoline", "Electric", "Gasoline", "Electric", "Diesel", "Gasoline"],
    "Transmission": ["Automatic", "Manual", "Automatic", "Automatic", "Manual", "Automatic", "Manual", "Automatic"],
    "Fuel Economy (mpg)": [28, 32, 30, 90, 35, 85, 28, 25]
})

# Define the UI
app_ui = ui.page_fluid(
    ui.h2("Car Filter and Fuel Economy Viewer"),
    
    # Dropdowns for filtering options
    ui.input_select("car_make", "Select Car Make", choices=list(data["Car Make"].unique()), selected="Toyota"),
    ui.input_select("fuel_type", "Select Fuel Type", choices=list(data["Fuel Type"].unique()), selected="Gasoline"),
    ui.input_select("transmission", "Select Transmission Type", choices=list(data["Transmission"].unique()), selected="Automatic"),
    
    # Outputs: filtered table and fuel economy summary
    ui.output_table("car_table"),
    ui.output_text("fuel_summary")
)

# Define server logic
def server(input, output, session):
    # Reactive table that filters data based on user selections
    @output
    @render.table
    def car_table():
        # Apply filters based on input values
        filtered_data = data[
            (data["Car Make"] == input.car_make()) &
            (data["Fuel Type"] == input.fuel_type()) &
            (data["Transmission"] == input.transmission())
        ]
        # Return filtered table
        return filtered_data if not filtered_data.empty else pd.DataFrame({"Message": ["No matching cars found."]})

    # Reactive text that shows the average fuel economy
    @output
    @render.text
    def fuel_summary():
        # Filter data based on input values
        filtered_data = data[
            (data["Car Make"] == input.car_make()) &
            (data["Fuel Type"] == input.fuel_type()) &
            (data["Transmission"] == input.transmission())
        ]
        # Calculate average fuel economy or display message if no matches
        if not filtered_data.empty:
            avg_fuel_economy = filtered_data["Fuel Economy (mpg)"].mean()
            return f"Average Fuel Economy: {avg_fuel_economy:.1f} mpg"
        else:
            return "No matching cars found."

# Create and run the Shiny app
app = App(app_ui, server)
