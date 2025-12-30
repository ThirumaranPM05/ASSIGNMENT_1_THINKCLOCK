import pandas as pd
import numpy as np
from impedance.models.circuits import CustomCircuit
import plotly.graph_objects as go

def analyze_impedance(csv_path):

    # ---------- Read & clean CSV ----------
    df = pd.read_csv(csv_path, header=None)
    df = df.iloc[:, :3]

    df[0] = pd.to_numeric(df[0], errors="coerce")
    df[1] = pd.to_numeric(df[1], errors="coerce")
    df[2] = pd.to_numeric(df[2], errors="coerce")

    df = df.dropna()

    freq = df[0].values
    z_real = df[1].values
    z_imag = df[2].values

    Z = z_real + 1j * z_imag

    valid = freq > 0
    freq = freq[valid]
    Z = Z[valid]

    if len(freq) == 0:
        raise ValueError("No valid EIS data after preprocessing")

    # ---------- Equivalent Circuit ----------
    circuit = "R0-p(R1,CPE1)-W1"
    initial_guess = [0.01, 0.02, 1e-5, 0.8, 0.01]

    model = CustomCircuit(circuit, initial_guess=initial_guess)
    model.fit(freq, Z)

    params = model.parameters_

    # ---------- SoH ----------
    Rb_current = params[0]
    Rb_max = 0.05
    soh = (Rb_current / Rb_max) * 100

    # ---------- Bode Plot (CRITICAL PART) ----------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=freq.tolist(),                 # ✅ force JSON-safe
        y=np.abs(Z).tolist(),             # ✅ force JSON-safe
        mode="lines+markers",
        name="|Z|"
    ))

    fig.update_xaxes(
        type="log",
        title="Frequency (Hz)"
    )

    fig.update_yaxes(
        title="Impedance Magnitude (Ohm)"
    )

    fig.update_layout(
        title="Bode Plot (EIS)",
        template="plotly_white"
    )

    return {
        "Rb": round(params[0], 5),
        "R_SEI": round(params[1], 5),
        "CPE_SEI": round(params[2], 5),
        "R_CT": round(params[3], 5),
        "Warburg": round(params[4], 5)
    }, round(soh, 2), fig.to_json()
