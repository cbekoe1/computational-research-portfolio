# Wake Effects in a 3×3 Wind Farm  
_Project 2 — Computational Wind Farm Modeling_  
**Author:** Collins Bekoe  
**Date:** February 02, 2026  

---

## Executive Summary

Wind farms are complex systems where turbine interactions can dramatically affect performance. This project models wake effects in a 3×3 wind farm using the Jensen and Larsen wake models, visualizes wake and turbulence fields, performs sensitivity and directional analyses, and applies a greedy layout optimization to improve total power output. The results show that wake-aware design and layout optimization can significantly enhance farm efficiency.

---

## 1. Introduction

In wind farms, upstream turbines extract energy from the wind, creating wakes that reduce wind speed and increase turbulence for downstream machines. These wake effects lead to lower power output and higher mechanical stress, making layout design a critical challenge.

This project builds a modular simulation framework to analyze wake behavior in a 3×3 wind farm. The goals are:

- Understand how wakes affect turbine performance  
- Visualize wake and turbulence fields  
- Quantify sensitivity to layout and wind conditions  
- Compare wake models  
- Optimize turbine layout to improve total power  

---

## 2. Modeling Approach

### 2.1 Farm Configuration

The baseline layout is a 3×3 grid of identical turbines spaced at 5D intervals. Turbine specs (rotor diameter, thrust coefficient, rated power) are loaded from a JSON file. All simulations assume uniform inflow wind speed and constant wake expansion coefficient.

### 2.2 Wake Modeling

The Jensen model computes velocity deficits using a linearly expanding wake cone. Wake overlaps are combined using root-sum-square logic. Power is estimated using a cubic relationship with effective wind speed, capped at rated power.

The Larsen model offers an alternative formulation with different wake recovery behavior. Both models are used to compare predictions.

### 2.3 Turbulence Modeling

Wake-added turbulence is modeled empirically. Ambient turbulence intensity is specified, and wake-induced contributions are superimposed where wakes overlap.

### 2.4 Sensitivity Analysis

Farm power is evaluated across variations in:

- Turbine spacing  
- Inflow wind speed  
- Wake expansion coefficient  

This reveals how layout and environmental factors influence performance.

### 2.5 Directional Analysis

To simulate different wind directions, turbine coordinates are rotated while keeping wind aligned with the x-axis. Simulations are run for 0°, 30°, 60°, and 90°.

### 2.6 Layout Optimization

A greedy search algorithm perturbs turbine positions to reduce wake overlap. Moves are accepted only if they increase total farm power. The process tracks best-so-far performance and outputs an optimized layout.

---

## 3. Results

### 3.1 Wake Contours

The wake field shows strong deficits behind upstream turbines and compounded losses downstream.

![Wake Contours](results/wake_contour.png)

---

### 3.2 Turbulence Intensity

Turbulence increases downstream due to wake interactions. Upstream turbines experience only ambient levels.

![Turbulence Field](results/turbulence_field.png)  
![Turbulence vs Distance](results/turbulence_vs_distance.png)

---

### 3.3 Sensitivity Analysis

Farm power increases with spacing and wind speed, and varies with wake expansion coefficient.

![Power vs Spacing](results/power_vs_spacing.png)  
![Power vs Wind Speed](results/power_vs_windspeed.png)  
![Power vs k Factor](results/power_vs_kfactor.png)

---

### 3.4 Directional Effects

Farm performance depends heavily on wind direction. Wake maps show how overlap shifts with angle.

![Power vs Wind Direction](results/power_vs_wind_direction.png)

Wake maps:

- 0°:  
  ![](results/directional_wake_maps/wake_map_0deg.png)
- 30°:  
  ![](results/directional_wake_maps/wake_map_30deg.png)
- 60°:  
  ![](results/directional_wake_maps/wake_map_60deg.png)
- 90°:  
  ![](results/directional_wake_maps/wake_map_90deg.png)

---

### 3.5 Jensen vs Larsen Comparison

Both models predict similar trends, but differ in wake recovery and downstream power estimates.

![Jensen vs Larsen Power](results/total_power_jensen_vs_larsen.png)

---

### 3.6 Layout Optimization

The greedy optimizer significantly improves total farm power by reducing wake overlap.

- Optimization progress:  
  ![](results/optimization_progress.png)

- Initial vs optimized layout:  
  ![](results/optimized_layout.png)

- Direct power comparison:  
  ![](results/initial_vs_optimized_power.png)

---

## 4. Discussion

This study confirms that wake effects are central to wind farm performance. Key insights:

- Compact layouts suffer from compounded wake losses  
- Turbulence intensity varies across the farm, affecting fatigue loading  
- Wind direction dramatically alters wake interactions  
- Wake model choice affects energy yield estimates  
- Even simple optimization can yield large performance gains  

The optimized layout increased total farm power from **15,042 kW to 25,882 kW**, a 72% improvement.

---

## 5. Conclusion

This project demonstrates a complete computational workflow for wake-aware wind farm modeling. It combines physical modeling, simulation, visualization, and optimization to produce actionable design insights.

The framework is modular, reproducible, and ready for extension to larger farms, probabilistic wind climates, and more advanced optimization strategies.

