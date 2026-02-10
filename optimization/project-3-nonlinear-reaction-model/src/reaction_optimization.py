import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# -----------------------------
# 1. True model and synthetic data
# -----------------------------
def reaction_model(t, A, k):
    return -k * A

def solve_reaction(k, A0=1.0, t_eval=None):
    sol = solve_ivp(
        fun=lambda t, y: reaction_model(t, y, k),
        t_span=(0, 10),
        y0=[A0],
        t_eval=t_eval
    )
    return sol.y[0]

t_eval = np.linspace(0, 10, 50)
k_true = 0.35
A_true = solve_reaction(k_true, t_eval=t_eval)

# Add noise
rng = np.random.default_rng(42)
noise = rng.normal(0, 0.02, size=len(A_true))
A_obs = A_true + noise

df = pd.DataFrame({"t": t_eval, "A_obs": A_obs})
df.to_csv("../data/reaction_data.csv", index=False)

# -----------------------------
# 2. Parameter estimation
# -----------------------------
def residuals(k):
    A_pred = solve_reaction(k[0], t_eval=t_eval)
    return A_pred - A_obs

res = least_squares(residuals, x0=[0.1], bounds=(0, 5))
k_est = res.x[0]

# Save estimated parameter
with open("../results/estimated_k.txt", "w") as f:
    f.write(f"Estimated k: {k_est:.4f}\n")
    f.write(f"True k: {k_true:.4f}\n")

# -----------------------------
# 3. Sensitivity analysis
# -----------------------------
k_values = np.linspace(k_est * 0.5, k_est * 1.5, 20)
errors = []

for k in k_values:
    A_pred = solve_reaction(k, t_eval=t_eval)
    mse = np.mean((A_pred - A_obs)**2)
    errors.append(mse)

# -----------------------------
# 4. Plots
# -----------------------------
# Fit vs data
A_fit = solve_reaction(k_est, t_eval=t_eval)

plt.figure(figsize=(8, 5))
plt.scatter(t_eval, A_obs, label="Observed", color="black")
plt.plot(t_eval, A_fit, label=f"Fitted model (k={k_est:.3f})", color="red")
plt.plot(t_eval, A_true, label="True model", color="blue", linestyle="--")
plt.xlabel("Time")
plt.ylabel("Concentration A(t)")
plt.title("Reaction Model Fit")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/model_fit.png", dpi=300)
plt.close()

# Sensitivity curve
plt.figure(figsize=(8, 5))
plt.plot(k_values, errors, "-o")
plt.xlabel("k value")
plt.ylabel("Mean squared error")
plt.title("Sensitivity of Fit to Reaction Rate Constant")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/sensitivity_curve.png", dpi=300)
plt.close()
