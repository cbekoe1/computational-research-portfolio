import matplotlib.pyplot as plt
import numpy as np

def plot_power_distribution(power_output: np.ndarray):
    """
    Plot histogram of simulated power output.
    """
    plt.figure(figsize=(10, 5))
    plt.hist(power_output, bins=40, color="skyblue", edgecolor="black")
    plt.title("Distribution of Wind Turbine Power Output")
    plt.xlabel("Power (kW)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def plot_power_curve(power_curve: dict):
    """
    Plot the turbine power curve.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(power_curve["speed"], power_curve["power"], marker="o")
    plt.title("Turbine Power Curve")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Power (kW)")
    plt.grid(True)
    plt.show()