import matplotlib.pyplot as plt

def plot_farm_layout(turbines, filename=None):
    xs = [t.x for t in turbines]
    ys = [t.y for t in turbines]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, c="tab:blue")
    for i, t in enumerate(turbines):
        plt.text(t.x + 20, t.y + 20, f"T{i+1}", fontsize=9)

    plt.xlabel("x [m] (wind from left to right)")
    plt.ylabel("y [m]")
    plt.title("Wind Farm Layout (3x3 Grid)")
    plt.axis("equal")
    plt.grid(True)

    if filename is not None:
        plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()

def plot_power_bar(turbines, powers_kw, filename=None):
    labels = [f"T{i+1}" for i in range(len(turbines))]
    plt.figure(figsize=(8, 4))
    plt.bar(labels, powers_kw, color="tab:green")
    plt.ylabel("Power [kW]")
    plt.title("Turbine Power Output with Wake Effects")
    plt.grid(axis="y", alpha=0.3)

    if filename is not None:
        plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()
