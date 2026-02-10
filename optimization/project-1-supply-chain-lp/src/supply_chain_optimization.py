import pandas as pd
import matplotlib.pyplot as plt
import pulp
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Define supply, demand, and costs
plants = ["Plant_A", "Plant_B"]
warehouses = ["WH_1", "WH_2", "WH_3"]

supply = {
    "Plant_A": 100,
    "Plant_B": 120
}

demand = {
    "WH_1": 80,
    "WH_2": 70,
    "WH_3": 60
}

costs = {
    ("Plant_A", "WH_1"): 4,
    ("Plant_A", "WH_2"): 6,
    ("Plant_A", "WH_3"): 9,
    ("Plant_B", "WH_1"): 5,
    ("Plant_B", "WH_2"): 4,
    ("Plant_B", "WH_3"): 7
}

# Save input data
cost_df = pd.DataFrame(
    [(p, w, c) for (p, w), c in costs.items()],
    columns=["plant", "warehouse", "cost"]
)
cost_df.to_csv("../data/cost_matrix.csv", index=False)

# Define LP problem
prob = pulp.LpProblem("Supply_Chain_Transportation", pulp.LpMinimize)

# Decision variables: shipped quantity from plant p to warehouse w
x = pulp.LpVariable.dicts(
    "ship",
    ((p, w) for p in plants for w in warehouses),
    lowBound=0,
    cat="Continuous"
)

# Objective: minimize total cost
prob += pulp.lpSum(costs[(p, w)] * x[(p, w)] for p in plants for w in warehouses)

# Supply constraints
for p in plants:
    prob += pulp.lpSum(x[(p, w)] for w in warehouses) <= supply[p], f"supply_{p}"

# Demand constraints
for w in warehouses:
    prob += pulp.lpSum(x[(p, w)] for p in plants) >= demand[w], f"demand_{w}"

# Solve
prob.solve(pulp.PULP_CBC_CMD(msg=False))

# Extract results
solution = []
for p in plants:
    for w in warehouses:
        qty = x[(p, w)].varValue
        solution.append((p, w, qty, costs[(p, w)]))

sol_df = pd.DataFrame(solution, columns=["plant", "warehouse", "quantity", "unit_cost"])
sol_df["total_cost"] = sol_df["quantity"] * sol_df["unit_cost"]
sol_df.to_csv("../data/optimal_solution.csv", index=False)

total_cost = pulp.value(prob.objective)
with open("../results/total_cost.txt", "w") as f:
    f.write(f"Total transportation cost: {total_cost:.2f}\n")

# Pivot for visualization
pivot = sol_df.pivot(index="plant", columns="warehouse", values="quantity")

# Heatmap of shipped quantities
plt.figure(figsize=(6, 4))
im = plt.imshow(pivot.values, cmap="Blues")
plt.colorbar(im, label="Shipped quantity")
plt.xticks(range(len(warehouses)), warehouses)
plt.yticks(range(len(plants)), plants)
plt.title("Optimal Shipment Quantities")
plt.tight_layout()
plt.savefig("../results/shipment_heatmap.png", dpi=300)
plt.close()

# Bar plot of total shipped per plant and received per warehouse
plant_totals = sol_df.groupby("plant")["quantity"].sum()
wh_totals = sol_df.groupby("warehouse")["quantity"].sum()

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plant_totals.plot(kind="bar", color="steelblue")
plt.title("Total Shipped per Plant")
plt.ylabel("Quantity")

plt.subplot(1, 2, 2)
wh_totals.plot(kind="bar", color="darkorange")
plt.title("Total Received per Warehouse")
plt.ylabel("Quantity")

plt.tight_layout()
plt.savefig("../results/flow_summary.png", dpi=300)
plt.close()
