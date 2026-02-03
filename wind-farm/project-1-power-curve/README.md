# Project 1 – Wind Turbine Power Curve Simulation

## Overview

This project simulates the expected power output of a single wind turbine using:

- A Weibull wind speed distribution  
- A simplified turbine power curve  
- Monte Carlo simulation  
- Visualization of power output distribution  

It is the first project in a broader computational research portfolio focused on wind energy and related systems.

## Methods

- **Wind speed model:** Weibull distribution with shape parameter \(k\) and scale parameter \(c\)  
- **Power curve:** Piecewise turbine power curve with cut-in, rated, and cut-out speeds  
- **Simulation:**  
  - Generate many wind speed samples  
  - Interpolate power output from the power curve  
  - Analyze the resulting power distribution  

Core logic is implemented in `src/model.py`, `src/simulation.py`, and `src/utils.py`, with analysis in `notebooks/analysis.ipynb`.

## Results

- The simulated power output distribution is skewed, with most values near the rated power region.  
- The turbine power curve shows increasing power with wind speed up to the rated speed, then a plateau, and finally a drop at cut-out.  

These results illustrate how wind variability and turbine characteristics combine to shape expected energy production.

## Repository Structure

```text
project-1-power-curve/
├── data/          # (optional) input data files
├── notebooks/     # Jupyter notebooks (main analysis in analysis.ipynb)
├── report/        # Exported PDF report(s)
├── results/       # Generated figures, tables, or intermediate outputs
└── src/           # Core simulation and plotting code


## Report
The full research report is available in `report/`.

## Author
Collins Bekoe