import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

np.random.seed(42)

# -----------------------------
# 1. Synthetic asset returns
# -----------------------------
n_assets = 4
asset_names = ["Asset_A", "Asset_B", "Asset_C", "Asset_D"]
n_periods = 500  # e.g., 500 days

# True means and covariance
true_means = np.array([0.08, 0.10, 0.12, 0.15]) / 252  # daily
base_cov = np.array([
    [0.04, 0.02, 0.01, 0.00],
    [0.02, 0.05, 0.02, 0.01],
    [0.01, 0.02, 0.06, 0.03],
    [0.00, 0.01, 0.03, 0.09]
]) / (252**2)

returns = np.random.multivariate_normal(true_means, base_cov, size=n_periods)
df = pd.DataFrame(returns, columns=asset_names)
df.to_csv("../data/asset_returns.csv", index=False)

mu = df.mean().values  # estimated mean returns
Sigma = df.cov().values  # estimated covariance

# -----------------------------
# 2. Efficient frontier via QP
# -----------------------------
solvers.options["show_progress"] = False

def solve_markowitz(target_return=None, lam=None):
    """
    Either:
    - lam: risk aversion parameter (min lam*w'Σw - mu'w)
    - target_return: equality constraint on expected return
    """
    n = len(mu)
    P = matrix(2 * Sigma)
    q = matrix(np.zeros(n))

    # Constraints: sum w = 1, w >= 0
    G = matrix(-np.eye(n))
    h = matrix(np.zeros(n))
    A = matrix(1.0, (1, n))
    b = matrix(1.0)

    if target_return is not None:
        # Add return constraint: mu'w = target_return
        A_full = matrix(np.vstack([np.ones(n), mu]), (2, n), "d")
        b_full = matrix([1.0, target_return])
        sol = solvers.qp(P, q, G, h, A_full, b_full)
    elif lam is not None:
        # Risk aversion formulation: min lam*w'Σw - mu'w
        P_l = matrix(2 * lam * Sigma)
        q_l = matrix(-mu)
        sol = solvers.qp(P_l, q_l, G, h, A, b)
    else:
        raise ValueError("Provide either target_return or lam")

    w = np.array(sol["x"]).flatten()
    return w

# Efficient frontier: sweep target returns
target_returns = np.linspace(mu.min(), mu.max(), 30)
frontier_r = []
frontier_sigma = []
frontier_w = []

for r_target in target_returns:
    w = solve_markowitz(target_return=r_target)
    frontier_w.append(w)
    portfolio_return = np.dot(mu, w)
    portfolio_var = np.dot(w, Sigma @ w)
    frontier_r.append(portfolio_return)
    frontier_sigma.append(np.sqrt(portfolio_var))

frontier_r = np.array(frontier_r)
frontier_sigma = np.array(frontier_sigma)
frontier_w = np.array(frontier_w)

# Minimum-variance portfolio (smallest sigma)
idx_min_var = np.argmin(frontier_sigma)
w_min_var = frontier_w[idx_min_var]
r_min_var = frontier_r[idx_min_var]
sigma_min_var = frontier_sigma[idx_min_var]

# A mid-risk portfolio (e.g., middle of frontier)
idx_mid = len(target_returns) // 2
w_mid = frontier_w[idx_mid]
r_mid = frontier_r[idx_mid]
sigma_mid = frontier_sigma[idx_mid]

# Save weights
weights_df = pd.DataFrame(frontier_w, columns=asset_names)
weights_df["target_return"] = target_returns
weights_df["sigma"] = frontier_sigma
weights_df.to_csv("../data/efficient_frontier_weights.csv", index=False)

# -----------------------------
# 3. Plots
# -----------------------------
# Efficient frontier
plt.figure(figsize=(8, 5))
plt.plot(frontier_sigma * np.sqrt(252), frontier_r * 252, "-o", markersize=3, label="Efficient frontier")
plt.scatter(sigma_min_var * np.sqrt(252), r_min_var * 252, color="red", label="Min-variance")
plt.scatter(sigma_mid * np.sqrt(252), r_mid * 252, color="green", label="Example portfolio")
plt.xlabel("Annualized volatility")
plt.ylabel("Annualized return")
plt.title("Mean-Variance Efficient Frontier")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/efficient_frontier.png", dpi=300)
plt.close()

# Weights of min-variance portfolio
plt.figure(figsize=(6, 4))
plt.bar(asset_names, w_min_var, color="steelblue")
plt.ylabel("Weight")
plt.title("Minimum-Variance Portfolio Weights")
plt.tight_layout()
plt.savefig("../results/min_variance_weights.png", dpi=300)
plt.close()

# Weights of mid-risk portfolio
plt.figure(figsize=(6, 4))
plt.bar(asset_names, w_mid, color="darkorange")
plt.ylabel("Weight")
plt.title("Mid-Risk Portfolio Weights")
plt.tight_layout()
plt.savefig("../results/mid_risk_weights.png", dpi=300)
plt.close()
