import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from noise import pnoise2
import os

# Paths relative to running inside src/
DATA_PATH = "../data/terrain.npy"
MAP_PATH = "../results/terrain_map.png"
SURFACE_PATH = "../results/terrain_surface.png"

GRID_SIZE = 200
SCALE = 100.0
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

def generate_terrain(grid_size=GRID_SIZE):
    terrain = np.zeros((grid_size, grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            terrain[i][j] = pnoise2(i / SCALE,
                                    j / SCALE,
                                    octaves=OCTAVES,
                                    persistence=PERSISTENCE,
                                    lacunarity=LACUNARITY,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=42)
    
    terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
    return terrain

if __name__ == "__main__":
    terrain = generate_terrain()

    # Save terrain
    np.save(DATA_PATH, terrain)

    # 2D heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(terrain, cmap="terrain")
    plt.colorbar(label="Elevation")
    plt.title("Simulated Terrain Map")
    plt.savefig(MAP_PATH, dpi=300)
    plt.close()

    # 3D surface plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
    ax.plot_surface(X, Y, terrain, cmap=cm.terrain, linewidth=0, antialiased=False)
    ax.set_title("3D Terrain Surface")
    plt.savefig(SURFACE_PATH, dpi=300)
    plt.close()
