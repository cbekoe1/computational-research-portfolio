import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Age groups: children, adults, seniors
age_groups = ["0-19", "20-64", "65+"]

# Population distribution
N = np.array([300_000, 600_000, 100_000])
total_pop = N.sum()

# Epidemiological parameters
beta = 0.25
sigma = 1/5     # incubation period
gamma = 1/7     # infectious period

# Contact matrix (rows = infectee, cols = infector)
C = np.array([
    [8, 4, 1],
    [3, 7, 2],
    [1, 2, 4]
])

# Initial conditions
E0 = np.array([50, 50, 10])
I0 = np.array([20, 20, 5])
R0 = np.zeros(3)
S0 = N - E0 - I0 - R0

y0 = np.concatenate([S0, E0, I0, R0])

def seir_age_structured(t, y):
    S, E, I, R = np.split(y, 4)
    lambda_force = beta * (C @ (I / N))
    dS = -lambda_force * S
    dE = lambda_force * S - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return np.concatenate([dS, dE, dI, dR])

t_eval = np.linspace(0, 200, 400)

sol = solve_ivp(
    fun=seir_age_structured,
    t_span=(0, 200),
    y0=y0,
    t_eval=t_eval
)

S, E, I, R = np.split(sol.y, 4)

# Save data
np.save("../data/seir_age_structured.npy", sol.y)

# Plot infections by age group
plt.figure(figsize=(8, 6))
for idx, group in enumerate(age_groups):
    plt.plot(sol.t, I[idx], label=f"Infected {group}")
plt.xlabel("Time (days)")
plt.ylabel("Infected individuals")
plt.title("Age-Structured SEIR: Infections Over Time")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/infected_by_age.png", dpi=300)
plt.close()

# Plot total infections
plt.figure(figsize=(8, 6))
plt.plot(sol.t, I.sum(axis=0), color="black", linewidth=2)
plt.xlabel("Time (days)")
plt.ylabel("Total infected")
plt.title("Total Infections Across All Age Groups")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/total_infected.png", dpi=300)
plt.close()
