## ThinkClock Battery Diagnostic Web App

This project is a prototype web application for battery
diagnostics using Electrochemical Impedance Spectroscopy (EIS).

### Features
- Battery image upload
- Auto-generated 10-digit Cell ID
- Pre-filled meta & electrical parameters
- CSV upload for EIS data
- Equivalent Circuit Model (ECM) extraction
- State of Health (SoH) estimation

### Libraries Used
- Flask
- impedance.py
- Pandas, NumPy
- Plotly (optional)

### SoH Formula
SoH (%) = Rb(current) / Rb(max) × 100  
Rb_max is assumed as 0.05 ohm.

### Assumptions
- Simplified ECM
- Assumed min/max values for visualization

### Limitations
- Prototype-level accuracy
- Not chemistry-calibrated
