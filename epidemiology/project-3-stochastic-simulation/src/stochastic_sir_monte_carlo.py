import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

N = 10000
beta = 0.3
gamma = 1/10
I0 = 10
R0 = 0
S0 = N - I0 - R0

T = 160
n_runs = 200

def simulate_one_run():
    S = S0
    I = I0
    R = R0

    S_traj = [S]
    I_traj = [I]
    R_traj = [R]

    for t in range(T):
        if I == 0:
            S_traj.extend([S] * (T - t - 1))
            I_traj.extend([I] * (T - t - 1))
            R_traj.extend([R] * (T - t - 1))
            break

        p_inf = 1 - np.exp(-beta * I / N)
        p_rec = 1 - np.exp(-gamma)

        new_inf = np.random.binomial(S, p_inf)
        new_rec = np.random.binomial(I, p_rec)

        S = S - new_inf
        I = I + new_inf - new_rec
        R = R + new_rec

        S_traj.append(S)
        I_traj.append(I)
        R_traj.append(R)

    return np.array(S_traj), np.array(I_traj), np.array(R_traj)

final_sizes = []
sample_trajectories = []

for run in range(n_runs):
    S_traj, I_traj, R_traj = simulate_one_run()
    final_sizes.append(R_traj[-1])
    if run < 5:
        sample_trajectories.append((S_traj, I_traj, R_traj))

final_sizes = np.array(final_sizes)
np.savetxt("../data/final_sizes.csv", final_sizes, delimiter=",", header="final_size", comments="")

plt.figure(figsize=(8, 6))
for (S_traj, I_traj, R_traj) in sample_trajectories:
    t = np.arange(len(I_traj))
    plt.plot(t, I_traj, alpha=0.7)
plt.xlabel("Time (days)")
plt.ylabel("Infected individuals")
plt.title("Sample Stochastic Epidemic Trajectories")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/sample_trajectories.png", dpi=300)
plt.close()

plt.figure(figsize=(8, 6))
plt.hist(final_sizes, bins=20, edgecolor="black", alpha=0.8)
plt.xlabel("Final outbreak size (R(T))")
plt.ylabel("Frequency")
plt.title("Distribution of Final Outbreak Sizes (Monte Carlo)")
plt.tight_layout()
plt.savefig("../results/final_size_distribution.png", dpi=300)
plt.close()
