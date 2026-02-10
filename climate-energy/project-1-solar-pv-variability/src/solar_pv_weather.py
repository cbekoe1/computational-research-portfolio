import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# Time index: 7 days, 5-minute resolution
freq = "5min"
start = "2024-06-01 00:00"
end = "2024-06-08 00:00"
time_index = pd.date_range(start=start, end=end, freq=freq, inclusive="left")

df = pd.DataFrame(index=time_index)
df["day_of_year"] = df.index.dayofyear
df["hour"] = df.index.hour + df.index.minute / 60.0

# Simple clear-sky global horizontal irradiance (GHI) model
def clear_sky_ghi(hour):
    # sunrise ~5h, sunset ~21h, smooth bell
    ghi = np.maximum(0, np.sin((hour - 5) / (21 - 5) * np.pi))
    return ghi

df["clear_sky_ghi"] = clear_sky_ghi(df["hour"]) * 1000  # W/m^2 peak

# Synthetic cloud cover: 0 (clear) to 1 (overcast)
# Daily pattern + random variability
rng = np.random.default_rng(42)
base_cloud = 0.3 + 0.2 * np.sin(2 * np.pi * (df["day_of_year"] - df["day_of_year"].min()) / 7)
noise = rng.normal(0, 0.15, size=len(df))
df["cloud_cover"] = np.clip(base_cloud + noise, 0, 1)

# Effective irradiance after clouds
# Simple model: I_eff = (1 - 0.8 * cloud_cover) * clear_sky_ghi
df["ghi"] = (1 - 0.8 * df["cloud_cover"]) * df["clear_sky_ghi"]

# PV system parameters
pv_capacity_kw = 100.0      # 100 kW system
efficiency = 0.18           # module efficiency (lumped)
area_m2 = pv_capacity_kw * 1000 / (efficiency * 1000)  # rough scaling

# DC power output (very simple linear model)
# P = efficiency * area * GHI / 1000
df["pv_power_kw"] = efficiency * area_m2 * df["ghi"] / 1000.0
df["pv_power_kw"] = df["pv_power_kw"].clip(lower=0)

# Energy over time (kWh per interval)
dt_hours = 5 / 60.0
df["pv_energy_kwh"] = df["pv_power_kw"] * dt_hours

# Daily energy
daily_energy = df["pv_energy_kwh"].resample("D").sum()

# Save data
df.to_csv("../data/solar_pv_weather_timeseries.csv")
daily_energy.to_csv("../data/daily_energy.csv", header=["daily_pv_energy_kwh"])

# Plot 1: Clear-sky vs actual GHI for a representative day
one_day = df.loc["2024-06-03"]
plt.figure(figsize=(9, 5))
plt.plot(one_day.index, one_day["clear_sky_ghi"], label="Clear-sky GHI", color="orange", linewidth=2)
plt.plot(one_day.index, one_day["ghi"], label="Cloud-modified GHI", color="blue")
plt.ylabel("Irradiance (W/m²)")
plt.xlabel("Time")
plt.title("Clear-Sky vs Cloud-Modified Irradiance (Example Day)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/ghi_example_day.png", dpi=300)
plt.close()

# Plot 2: Cloud cover time series over the week
plt.figure(figsize=(9, 4))
plt.plot(df.index, df["cloud_cover"], color="gray")
plt.ylabel("Cloud cover (0–1)")
plt.xlabel("Time")
plt.title("Cloud Cover Over One Week")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/cloud_cover_week.png", dpi=300)
plt.close()

# Plot 3: PV power time series (full week)
plt.figure(figsize=(9, 5))
plt.plot(df.index, df["pv_power_kw"], color="green")
plt.ylabel("PV Power (kW)")
plt.xlabel("Time")
plt.title("PV Power Output Over One Week")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/pv_power_week.png", dpi=300)
plt.close()

# Plot 4: Daily energy bar chart
plt.figure(figsize=(7, 4))
plt.bar(daily_energy.index.strftime("%Y-%m-%d"), daily_energy.values, color="teal")
plt.ylabel("Daily PV Energy (kWh)")
plt.xlabel("Day")
plt.title("Daily PV Energy Production")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../results/daily_energy.png", dpi=300)
plt.close()
