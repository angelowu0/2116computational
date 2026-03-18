import pandas as pd
import plotly.graph_objects as go
import numpy as np

from utils.utils import get_ephemeris
from plotly.subplots import make_subplots

def plot_3i_uncertainty_ellipses():
    df_eph = get_ephemeris("3I", "2025-04-01", "2026-06-01", "1d")

    key_dates = ["2025-07-01", "2025-09-01", "2025-11-01", "2026-01-01", "2026-03-01"]

    fig = make_subplots(
        rows=len(key_dates), cols=1,
        subplot_titles=[f"Error Ellipse - {date}" for date in key_dates]
    )

    all_smaa = []  # collect all sizes to set a common scale

    for i, date in enumerate(key_dates, start=1):
        target = pd.Timestamp(date)
        idx = (df_eph["datetime"] - target).abs().idxmin()
        row = df_eph.loc[idx]

        if pd.isna(row["SMAA_3sigma"]):
            continue

        smaa = float(row["SMAA_3sigma"])
        smia = float(row["SMIA_3sigma"])
        theta = float(row["Theta_3sigma"])
        all_smaa.append(smaa)

        t = np.linspace(0, 2 * np.pi, 100)
        theta_rad = np.radians(theta)

        # Ellipse points
        x = smaa * np.cos(t)
        y = smia * np.sin(t)

        # Rotate
        x_rot = x * np.cos(theta_rad) - y * np.sin(theta_rad)
        y_rot = x * np.sin(theta_rad) + y * np.cos(theta_rad)

        # Centred on zero — not offset by RA/Dec
        fig.add_trace(go.Scatter(
            x=x_rot,
            y=y_rot,
            mode="lines",
            line=dict(color="cyan"),
            showlegend = False
        ), row=i, col=1)

        # Centre dot at origin
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode="markers",
            marker=dict(size=6, color="red"),
            showlegend=False
        ), row=i, col=1)

        fig.update_xaxes(title_text="arcsec", row=i, col=1)
        fig.update_yaxes(title_text="arcsec", row=i, col=1)

    # Set the same scale on all panels based on the largest ellipse
    max_size = max(all_smaa) * 1.5  # add 50% padding

    fig.update_xaxes(matches="x", range=[-max_size, max_size])
    fig.update_yaxes(matches="y", range=[-max_size, max_size], scaleanchor="x")

    fig.update_layout(
        title="3I/ATLAS - Error Ellipse Size Comparison",
        height=400 * len(key_dates),
        showlegend=True
    )

    fig.show()