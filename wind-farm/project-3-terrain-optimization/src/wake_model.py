import numpy as np
import matplotlib.pyplot as plt

# Load terrain + wind field
terrain = np.load("../data/terrain.npy")
wind_field = np.load("../data/wind_field.npy")

# Jensen wake model parameters
CT = 0.8            # thrust coefficient
k = 0.04            # wake decay constant
D = 100             # rotor diameter (m)

# Turbine layout (temporary for testing)
# These will be replaced by the optimizer later
turbine_positions = [
    (50, 50),
    (120, 60),
    (80, 140)
]

def jensen_wake(wind_field, turbines):
    ny, nx = wind_field.shape
    wake = np.zeros_like(wind_field)

    for (tx, ty) in turbines:
        U0 = wind_field[ty, tx]

        for y in range(ty, ny):
            dy = y - ty
            r = k * dy + D / 2

            for x in range(nx):
                dx = x - tx
                if abs(dx) <= r and dy > 0:
                    deficit = (1 - np.sqrt(1 - CT)) / (1 + k * dy / (D / 2))**2
                    wake[y, x] = max(wake[y, x], deficit * U0)

    return wake

if __name__ == "__main__":
    wake_field = jensen_wake(wind_field, turbine_positions)

    # Save wake field
    np.save("../data/wake_field.npy", wake_field)

    # Plot wake field
    plt.figure(figsize=(8, 6))
    plt.imshow(wake_field, cmap="inferno")
    plt.colorbar(label="Velocity Deficit (m/s)")
    plt.title("Wake Field (Jensen Model)")
    plt.savefig("../results/wake_field_map.png", dpi=300)
    plt.close()
