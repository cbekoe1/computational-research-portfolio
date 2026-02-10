import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Physical constants
C = 4.0e8  # effective heat capacity (J/m2/K)
S0 = 1361  # solar constant (W/m2)
alpha = 0.3  # planetary albedo
sigma = 5.67e-8  # Stefan-Boltzmann constant

# Radiative forcing from CO2
def forcing_co2(CO2, CO2_ref=280):
    return 5.35 * np.log(CO2 / CO2_ref)

# Energy balance equation
def dTdt(t, T, CO2):
    absorbed = (1 - alpha) * S0 / 4
    outgoing = sigma * T**4
    forcing = forcing_co2(CO2)
    return (absorbed - outgoing + forcing) / C

# CO2 scenarios
scenarios = {
    "Preindustrial (280 ppm)": 280,
    "Modern (420 ppm)": 420,
    "Doubled CO2 (560 ppm)": 560,
    "High Emissions (800 ppm)": 800
}

t_eval = np.linspace(0, 200, 500)  # years
results = {}

for label, CO2 in scenarios.items():
    sol = solve_ivp(
        fun=lambda t, T: dTdt(t, T, CO2),
        t_span=(0, 200),
        y0=[288],  # initial temperature (K)
        t_eval=t_eval
    )
    results[label] = sol.y[0]
    np.savetxt(f"../data/temp_{CO2}ppm.csv",
               np.vstack([sol.t, sol.y[0]]).T,
               delimiter=",",
               header="time,temperature_K",
               comments="")

# Plot temperature response
plt.figure(figsize=(9, 5))
for label, temps in results.items():
    plt.plot(t_eval, temps - 273.15, label=label)
plt.xlabel("Time (years)")
plt.ylabel("Temperature (°C)")
plt.title("Global Temperature Response to CO₂ Forcing")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/temperature_response.png", dpi=300)
plt.close()

# Plot equilibrium temperature vs CO2
CO2_vals = np.linspace(280, 1000, 200)
T_eq = []
for CO2 in CO2_vals:
    absorbed = (1 - alpha) * S0 / 4
    forcing = forcing_co2(CO2)
    T = ((absorbed + forcing) / sigma)**0.25
    T_eq.append(T - 273.15)

plt.figure(figsize=(8, 5))
plt.plot(CO2_vals, T_eq, color="red")
plt.xlabel("CO₂ concentration (ppm)")
plt.ylabel("Equilibrium Temperature (°C)")
plt.title("Equilibrium Climate Sensitivity Curve")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/equilibrium_curve.png", dpi=300)
plt.close()
