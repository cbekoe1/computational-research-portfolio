import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pulp
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# -----------------------------
# 1. Generate hourly load (1 month)
# -----------------------------
date_range = pd.date_range("2024-06-01", "2024-06-30 23:00", freq="h")
df = pd.DataFrame(index=date_range)

hours = df.index.hour
dayofweek = df.index.dayofweek

daily = 30 + 10 * np.sin(2 * np.pi * (hours - 7) / 24)
weekly = np.where(dayofweek < 5, 1.0, 0.9)

rng = np.random.default_rng(42)
noise = rng.normal(0, 1.5, len(df))

df["load_MW"] = (daily * weekly) + noise

# -----------------------------
# 2. Solar PV model (same horizon)
# -----------------------------
def clear_sky(hour):
    return np.maximum(0, np.sin((hour - 5) / (21 - 5) * np.pi))

df["hour_float"] = df.index.hour + df.index.minute / 60.0
df["clear_sky_ghi"] = clear_sky(df["hour_float"]) * 1000

base_cloud = 0.3 + 0.2 * np.sin(2 * np.pi * (df.index.day - 1) / 30)
cloud_noise = rng.normal(0, 0.15, len(df))
df["cloud_cover"] = np.clip(base_cloud + cloud_noise, 0, 1)

df["ghi"] = (1 - 0.8 * df["cloud_cover"]) * df["clear_sky_ghi"]

pv_capacity_MW = 50.0
efficiency = 0.18
area_m2 = pv_capacity_MW * 1e6 / (efficiency * 1000)

df["pv_MW"] = efficiency * area_m2 * df["ghi"] / 1e6
df["pv_MW"] = df["pv_MW"].clip(lower=0)

# -----------------------------
# 3. Net load
# -----------------------------
df["net_load_MW"] = (df["load_MW"] - df["pv_MW"]).clip(lower=0)

df.to_csv("../data/capstone_timeseries.csv")

# -----------------------------
# 4. Dispatch optimization
# -----------------------------
# Three thermal generators
gens = ["G1", "G2", "G3"]
max_cap = {"G1": 40, "G2": 60, "G3": 80}  # MW
min_cap = {"G1": 0, "G2": 0, "G3": 0}
cost = {"G1": 20, "G2": 30, "G3": 50}  # $/MWh

prob = pulp.LpProblem("Dispatch_Optimization", pulp.LpMinimize)

# Decision variables: generation g(h, unit)
gen = pulp.LpVariable.dicts(
    "gen",
    ((t, g) for t in df.index for g in gens),
    lowBound=0,
    cat="Continuous"
)

# Objective: sum_t sum_g cost_g * gen_g(t)
prob += pulp.lpSum(cost[g] * gen[(t, g)] for t in df.index for g in gens)

# Constraints: for each hour, meet net load
for t in df.index:
    prob += pulp.lpSum(gen[(t, g)] for g in gens) >= df.loc[t, "net_load_MW"], f"demand_{t}"

# Capacity constraints
for t in df.index:
    for g in gens:
        prob += gen[(t, g)] <= max_cap[g], f"max_{g}_{t}"
        prob += gen[(t, g)] >= min_cap[g], f"min_{g}_{t}"

prob.solve(pulp.PULP_CBC_CMD(msg=False))

# Extract dispatch
records = []
for t in df.index:
    row = {"time": t}
    for g in gens:
        row[g] = gen[(t, g)].varValue
    records.append(row)

dispatch_df = pd.DataFrame(records).set_index("time")
dispatch_df["total_gen_MW"] = dispatch_df[gens].sum(axis=1)
dispatch_df["net_load_MW"] = df["net_load_MW"]
dispatch_df.to_csv("../data/dispatch_results.csv")

total_cost = sum(
    dispatch_df[g] * cost[g] for g in gens
).sum()

with open("../results/total_cost.txt", "w") as f:
    f.write(f"Total generation cost over month: {total_cost:.2f} $\n")

# -----------------------------
# 5. Plots
# -----------------------------
# Load, PV, net load (sample week)
sample = df.iloc[:24*7]

plt.figure(figsize=(10, 5))
plt.plot(sample.index, sample["load_MW"], label="Load", color="black")
plt.plot(sample.index, sample["pv_MW"], label="PV", color="orange")
plt.plot(sample.index, sample["net_load_MW"], label="Net load", color="blue")
plt.ylabel("Power (MW)")
plt.xlabel("Time")
plt.title("Load, PV, and Net Load (Sample Week)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/load_pv_netload_week.png", dpi=300)
plt.close()

# Dispatch vs net load (same week)
dispatch_sample = dispatch_df.iloc[:24*7]

plt.figure(figsize=(10, 5))
plt.stackplot(
    dispatch_sample.index,
    [dispatch_sample[g] for g in gens],
    labels=gens,
    colors=["#4C72B0", "#55A868", "#C44E52"],
    alpha=0.8
)
plt.plot(dispatch_sample.index, dispatch_sample["net_load_MW"], color="black", linewidth=1.5, label="Net load")
plt.ylabel("Power (MW)")
plt.xlabel("Time")
plt.title("Generator Dispatch vs Net Load (Sample Week)")
plt.legend(loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/dispatch_vs_netload_week.png", dpi=300)
plt.close()

# PV contribution histogram
pv_share = (df["pv_MW"] / df["load_MW"]).clip(lower=0, upper=1)
plt.figure(figsize=(6, 4))
plt.hist(pv_share, bins=20, edgecolor="black")
plt.xlabel("PV share of load")
plt.ylabel("Frequency")
plt.title("Distribution of PV Contribution to Load")
plt.tight_layout()
plt.savefig("../results/pv_share_hist.png", dpi=300)
plt.close()
