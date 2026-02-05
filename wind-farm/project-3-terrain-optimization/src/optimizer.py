import numpy as np
import matplotlib.pyplot as plt
import pygad

# Load data
terrain = np.load("../data/terrain.npy")
wind_field = np.load("../data/wind_field.npy")

# Import wake model
from wake_model import jensen_wake

GRID_SIZE = terrain.shape[0]
N_TURBINES = 5
MIN_SPACING = 20  # minimum distance between turbines (grid units)

# --- ENERGY MODEL ---------------------------------------------------------

def compute_energy(layout):
    turbines = [(int(layout[i]), int(layout[i+1])) for i in range(0, len(layout), 2)]
    wake = jensen_wake(wind_field, turbines)
    effective_wind = wind_field - wake
    effective_wind = np.clip(effective_wind, 0, None)

    # Power ~ U^3 (simplified)
    power = 0
    for (x, y) in turbines:
        power += effective_wind[y, x] ** 3

    return power

# --- CONSTRAINTS ----------------------------------------------------------

def spacing_penalty(layout):
    turbines = [(int(layout[i]), int(layout[i+1])) for i in range(0, len(layout), 2)]
    penalty = 0

    for i in range(len(turbines)):
        for j in range(i+1, len(turbines)):
            x1, y1 = turbines[i]
            x2, y2 = turbines[j]
            dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if dist < MIN_SPACING:
                penalty += (MIN_SPACING - dist) * 1000

    return penalty

# --- FITNESS FUNCTION -----------------------------------------------------

def fitness_func(ga_instance, solution, solution_idx):
    energy = compute_energy(solution)
    penalty = spacing_penalty(solution)
    return energy - penalty

# --- GA SETUP -------------------------------------------------------------

gene_space = list(range(GRID_SIZE))

ga = pygad.GA(
    num_generations=40,
    num_parents_mating=8,
    fitness_func=fitness_func,
    sol_per_pop=20,
    num_genes=N_TURBINES * 2,
    gene_space=gene_space,
    mutation_percent_genes=20,
    mutation_type="random",
    crossover_type="single_point",
    keep_parents=2
)

# --- RUN GA ---------------------------------------------------------------

ga.run()

solution, fitness, _ = ga.best_solution()

# Save optimal layout
np.save("../data/optimal_layout.npy", solution)

# Convert layout to coordinate pairs
turbines_initial = [(int(ga.initial_population[0][i]),
                     int(ga.initial_population[0][i+1]))
                    for i in range(0, N_TURBINES*2, 2)]

turbines_optimal = [(int(solution[i]), int(solution[i+1]))
                    for i in range(0, N_TURBINES*2, 2)]

# --- PLOTS ----------------------------------------------------------------

# Initial layout
plt.figure(figsize=(6, 6))
plt.imshow(terrain, cmap="terrain")
for (x, y) in turbines_initial:
    plt.scatter(x, y, c="red", s=50)
plt.title("Initial Turbine Layout")
plt.savefig("../results/initial_layout.png", dpi=300)
plt.close()

# Optimized layout
plt.figure(figsize=(6, 6))
plt.imshow(terrain, cmap="terrain")
for (x, y) in turbines_optimal:
    plt.scatter(x, y, c="blue", s=50)
plt.title("Optimized Turbine Layout")
plt.savefig("../results/optimized_layout.png", dpi=300)
plt.close()

# Fitness curve 
plt.figure()
fig = ga.plot_fitness(title="GA Fitness Curve")
fig.savefig("../results/fitness_curve.png", dpi=300)
plt.close(fig)


