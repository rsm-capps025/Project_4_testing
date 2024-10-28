import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from shiny import App, ui, render, reactive

# Prepare data and model
data = pd.DataFrame({
    'Age': [25, 30, 35, 40, 45, 50],
    'Weight': [150, 160, 170, 180, 190, 200],
    'Secretor_y': [0, 1, 0, 1, 0, 1]
})  # Example data, replace with your actual dataset

# Data cleaning
input_variables = ['Age', 'Weight']
data_cleaned = data.dropna(subset=input_variables + ['Secretor_y'])
X = data_cleaned[input_variables].values
y = data_cleaned['Secretor_y'].values

# Initialize and train the KNN model
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X, y)

# Define UI for the Shiny app
app_ui = ui.page_fluid(
    ui.h2("KNN Model Prediction App"),
    
    # Inputs for Age and Weight
    ui.input_slider("age", "Age:", min(X[:, 0]), max(X[:, 0]), 30),
    ui.input_slider("weight", "Weight:", min(X[:, 1]), max(X[:, 1]), 160),
    
    # Output area for predictions
    ui.output_text("prediction_text"),
    
    # Output area for scatter plot
    ui.output_plot("scatter_plot")
)

# Server logic
def server(input, output, session):
    
    # Reactive to make predictions based on slider inputs
    @reactive.Calc
    def prediction():
        X_new = np.array([[input.age(), input.weight()]])
        prediction = knn.predict(X_new)
        return prediction[0]
    
    # Display the prediction
    @output
    @render.text
    def prediction_text():
        return f"Predicted Secretor_y for input values: {prediction()}"
    
    # Render scatter plot with training data and prediction point
    @output
    @render.plot
    def scatter_plot():
        plt.figure(figsize=(8, 6))
        
        # Define custom colormap and norm for discrete values
        cmap = ListedColormap(['blue', 'red'])
        norm = BoundaryNorm([0, 0.5, 1], cmap.N)  # Discrete boundaries for 0 and 1
        
        # Scatter plot for existing data with discrete color mapping
        scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap, norm=norm, edgecolor='k', label='Training Data')
        
        # Plot new prediction point
        plt.scatter(input.age(), input.weight(), c='black', marker='x', s=100, label='New Prediction')
        
        # Label the plot
        plt.xlabel('Age')
        plt.ylabel('Weight')
        
        # Create color bar with custom labels
        cbar = plt.colorbar(scatter, ticks=[0, 1])
        cbar.ax.set_yticklabels(['Non-Secretor', 'Secretor'])
        plt.legend()
        plt.title('KNN Classification with New Data Point')
        plt.grid(True)
        
    return prediction_text, scatter_plot

# Create and run the app
app = App(app_ui, server)
