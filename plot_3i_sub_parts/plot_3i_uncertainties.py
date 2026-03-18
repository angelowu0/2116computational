from utils.utils import get_ephemeris
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.ndimage import gaussian_filter1d
import numpy as np

def plot_3i_uncertainties():
    df_eph = get_ephemeris("3I", "2025-04-01", "2026-06-01", "1d")

    # Gaussian smoothing then gradient
    smoothed = gaussian_filter1d(df_eph["RSS_3sigma"].values, sigma=3)
    df_eph["sigma_growth"] = np.gradient(smoothed, df_eph["datetime_jd"].values)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Growth Rate","Position Uncertainty"))

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["sigma_growth"],
        name="Change in Total uncertainty (RSS)",
        line=dict(color="cyan")
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["RSS_3sigma"],
        name="Total uncertainty (RSS)",
        line=dict(color="cyan")
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["SMAA_3sigma"],
        name="Semi-major axis",
        line=dict(color="orange")
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["SMIA_3sigma"],
        name="Semi-minor axis",
        line=dict(color="yellow")
    ), row=2, col=1)

    fig.update_yaxes(title_text="Uncertainty (arcsec)",type="log", row=2, col=1)
    fig.update_yaxes(title_text="Change per day (arcsec)", row=1, col=1)

    fig.show()