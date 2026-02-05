import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

# Ensure folders exist
os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Total population
N = 1_000_000

# Epidemiological parameters
beta = 0.3      # transmission rate
gamma = 1/10    # recovery rate (10 days infectious)

# Vaccination scenarios (fraction of population vaccinated at t=0)
vaccination_rates = [0.0, 0.2, 0.5, 0.7]

# Time span (days)
t_start, t_end = 0, 160
t_eval = np.linspace(t_start, t_end, 400)

def sir_with_vaccination(t, y, beta, gamma, N):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

results = {}

for v in vaccination_rates:
    # Initial conditions
    V = v * N
    I0 = 100.0
    R0 = 0.0
    S0 = N - V - I0 - R0

    y0 = [S0, I0, R0]

    sol = solve_ivp(
        fun=lambda t, y: sir_with_vaccination(t, y, beta, gamma, N),
        t_span=(t_start, t_end),
        y0=y0,
        t_eval=t_eval
    )

    results[v] = {
        "t": sol.t,
        "S": sol.y[0],
        "I": sol.y[1],
        "R": sol.y[2]
    }

    # Save time series to data
    data_arr = np.vstack([sol.t, sol.y[0], sol.y[1], sol.y[2]]).T
    np.savetxt(f"../data/sir_vaccination_v{int(v*100)}.csv",
               data_arr,
               delimiter=",",
               header="t,S,I,R",
               comments="")

# Plot: infection curves for all vaccination scenarios
plt.figure(figsize=(8, 6))
for v in vaccination_rates:
    plt.plot(results[v]["t"], results[v]["I"], label=f"Vaccination {int(v*100)}%")
plt.xlabel("Time (days)")
plt.ylabel("Infected individuals")
plt.title("SIR Dynamics Under Different Vaccination Rates")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../results/infected_vs_time_vaccination.png", dpi=300)
plt.close()

# Plot: S, I, R for a selected scenario (e.g., 0% and 50%)
for v in [0.0, 0.5]:
    t = results[v]["t"]
    S = results[v]["S"]
    I = results[v]["I"]
    R = results[v]["R"]

    plt.figure(figsize=(8, 6))
    plt.plot(t, S, label="Susceptible")
    plt.plot(t, I, label="Infected")
    plt.plot(t, R, label="Recovered")
    plt.xlabel("Time (days)")
    plt.ylabel("Number of individuals")
    plt.title(f"SIR Trajectories (Vaccination {int(v*100)}%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"../results/sir_trajectories_v{int(v*100)}.png", dpi=300)
    plt.close()
