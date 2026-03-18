from utils.utils import get_vectors_for_3i_from
import pandas as pd
import plotly.graph_objects as go

def plot_3i_planet_distances():
    PLANETS = {
        "Sun": "10",
        "Earth": "399",
        "Mars": "499",
        "Jupiter": "599",
        "Saturn": "699",
    }

    COLOURS = {
        "Sun": "green",
        "Earth": "skyblue",
        "Mars": "red",
        "Jupiter": "orange",
        "Saturn": "gold",
    }

    fig = go.Figure()

    for i, (name, pid) in enumerate(PLANETS.items(), start=1):
        df_planet = get_vectors_for_3i_from(f"500@{pid}")
        df_planet = df_planet.reset_index(drop=True)

        idx_min = df_planet["range"].idxmin()
        closest_date = pd.Timestamp(df_planet.loc[idx_min, "datetime"])
        closest_dist = df_planet.loc[idx_min, "range"]

        date_start = closest_date - pd.DateOffset(months=16)
        date_end = closest_date + pd.DateOffset(months=16)

        df_window = df_planet[
            (df_planet["datetime"] >= date_start) &
            (df_planet["datetime"] <= date_end)
            ]

        fig.add_trace(go.Scatter(
            x=df_window["datetime"],
            y=df_window["range"],
            name=name,
            line=dict(color=COLOURS.get(name, "white"))
        ))

        fig.add_trace(go.Scatter(
            x=[closest_date],
            y=[closest_dist],
            mode="markers",
            marker=dict(size=12, color="red", symbol="star"),
            name="Closest approach"
        ))

    fig.update_xaxes(
        range=["2025-01-01", "2026-07-01"]
    )

    fig.update_layout(
        title=f"3I/ATLAS - Distances and Closest Approach from Planets and Sun",
        xaxis_title="Date",
        yaxis_title="Distance (AU)",
        height=1000
    )

    fig.show()