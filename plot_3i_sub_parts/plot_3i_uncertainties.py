from utils.utils import get_ephemeris
import plotly.graph_objects as go

def plot_3i_uncertainties():
    df_eph = get_ephemeris("3I", "2025-04-01", "2026-06-01", "1d")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["RSS_3sigma"],
        name="Total uncertainty (RSS)",
        line=dict(color="cyan")
    ))

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["SMAA_3sigma"],
        name="Semi-major axis",
        line=dict(color="orange")
    ))

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["SMIA_3sigma"],
        name="Semi-minor axis",
        line=dict(color="yellow")
    ))

    fig.update_layout(
        title="3I/ATLAS — Position Uncertainty Over Time",
        xaxis_title="Date",
        yaxis_title="3-sigma uncertainty (arcsec)",
        yaxis_type="log",
        height=500
    )

    fig.show()