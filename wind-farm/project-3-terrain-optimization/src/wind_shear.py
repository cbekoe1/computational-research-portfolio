import numpy as np
import matplotlib.pyplot as plt

# Load terrain
terrain = np.load("../data/terrain.npy")

# Parameters
U_ref = 8.0          # reference wind speed at z_ref
z_ref = 10.0         # reference height (m)
alpha = 0.15         # wind shear exponent (typical for open terrain)
hub_height = 80.0    # turbine hub height (m)

# Elevation-adjusted wind speed
def compute_wind_field(terrain):
    elevation = terrain * 200  # scale terrain to 0–200 m elevation
    effective_height = hub_height + elevation
    wind_field = U_ref * (effective_height / z_ref) ** alpha
    return wind_field

if __name__ == "__main__":
    wind_field = compute_wind_field(terrain)

    # Save wind field
    np.save("../data/wind_field.npy", wind_field)

    # Plot wind field
    plt.figure(figsize=(8, 6))
    plt.imshow(wind_field, cmap="viridis")
    plt.colorbar(label="Wind Speed (m/s)")
    plt.title("Elevation-Adjusted Wind Field")
    plt.savefig("../results/wind_field_map.png", dpi=300)
    plt.close()
