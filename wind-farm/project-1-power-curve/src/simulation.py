import numpy as np
from model import generate_wind_speeds

def load_power_curve() -> dict:
    """Returns a simple turbine power curve.

    Replace with real turbine data later if desired.
    """
    speeds = np.array([0, 3, 5, 8, 12, 15, 20, 25])  # m/s
    power = np.array([0, 0, 200, 800, 1500, 2000, 2000, 0])  # kW
    return {"speed": speeds, "power": power}


def simulate_power_output(wind_speeds: np.ndarray, power_curve: dict) -> np.ndarray:
    """Apply the turbine power curve to wind speeds using interpolation."""
    return np.interp(wind_speeds, power_curve["speed"], power_curve["power"])


def run_simulation(k: float, c: float, size: int = 10000) -> np.ndarray:
    """Full simulation pipeline: generate wind speeds, load power curve, compute output."""
    wind_speeds = generate_wind_speeds(k, c, size)
    curve = load_power_curve()
    power_output = simulate_power_output(wind_speeds, curve)
    return power_output