import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

os.makedirs("../results", exist_ok=True)
os.makedirs("../data", exist_ok=True)

# -----------------------------
# 1. Generate synthetic load data
# -----------------------------
date_range = pd.date_range("2022-01-01", "2023-12-31 23:00", freq="h")
df = pd.DataFrame(index=date_range)

# Base load shape: daily + weekly + seasonal
hours = df.index.hour
dayofweek = df.index.dayofweek
dayofyear = df.index.dayofyear

# Daily cycle
daily = 20 + 10 * np.sin(2 * np.pi * (hours - 7) / 24)

# Weekly cycle (lower weekends)
weekly = np.where(dayofweek < 5, 1.0, 0.85)

# Seasonal cycle (higher in winter)
seasonal = 1.0 + 0.2 * np.cos(2 * np.pi * (dayofyear - 15) / 365)

# Random noise
rng = np.random.default_rng(42)
noise = rng.normal(0, 1.5, len(df))

# Final load (MW)
df["load"] = (daily * weekly * seasonal) + noise

df.to_csv("../data/hourly_load.csv")

# -----------------------------
# 2. STL Decomposition
# -----------------------------
stl = STL(df["load"], period=24)
res = stl.fit()

plt.figure(figsize=(10, 8))
res.plot()
plt.tight_layout()
plt.savefig("../results/stl_decomposition.png", dpi=300)
plt.close()

# -----------------------------
# 3. Train-test split
# -----------------------------
train = df.iloc[:-24*30]
test = df.iloc[-24*30:]

# -----------------------------
# 4. ARIMA model
# -----------------------------
model = ARIMA(train["load"], order=(3, 1, 3))
fit = model.fit()

forecast = fit.forecast(steps=len(test))
forecast.index = test.index

# -----------------------------
# 5. Error metrics
# -----------------------------
mae = mean_absolute_error(test["load"], forecast)
rmse = np.sqrt(mean_squared_error(test["load"], forecast))

with open("../results/error_metrics.txt", "w") as f:
    f.write(f"MAE: {mae:.3f}\n")
    f.write(f"RMSE: {rmse:.3f}\n")

# -----------------------------
# 6. Plot forecast vs actual
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(train.index, train["load"], label="Train", color="gray", alpha=0.6)
plt.plot(test.index, test["load"], label="Actual", color="black")
plt.plot(forecast.index, forecast, label="Forecast", color="red")
plt.title("Electricity Load Forecast (ARIMA)")
plt.ylabel("Load (MW)")
plt.xlabel("Time")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("../results/forecast_vs_actual.png", dpi=300)
plt.close()

# -----------------------------
# 7. Save forecast
# -----------------------------
forecast_df = pd.DataFrame({"actual": test["load"], "forecast": forecast})
forecast_df.to_csv("../data/forecast_results.csv")
