from utils.utils import get_ephemeris
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numpy import cumsum
def plot_3i_observability():
    start = "2025-06-01"   # before perihelion
    stop  = "2027-01-01"   # well after, comet is ~10 AU out by then
    step  = "1d"

    df_eph = get_ephemeris("3I", start, stop, step)

    # Compute a simple observability score
    # Higher = better

    df_eph["observable"] = (
        (df_eph["elong"] > 30) &      # not too close to Sun
        (df_eph["Tmag"] < 20)         # bright enough for a large telescope
    ).astype(int)

    # Find contiguous observable windows
    df_eph["window_id"] = (df_eph["observable"].diff() != 0).cumsum()
    windows = df_eph[df_eph["observable"] == 1].groupby("window_id").agg(
        start=("datetime", "first"),
        end=("datetime", "last"),
        best_mag=("Tmag", "min"),
        min_elong=("elong", "min")
    ).reset_index(drop=True)

    print("Observable windows:")
    print(windows.to_string())

    # Plot observability
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=(
                            "Predicted Magnitude (lower = brighter)",
                            "Solar Elongation (degrees)",
                            "Observability"
                        ))

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["Tmag"],
        line=dict(color="yellow"),
        showlegend=False
    ), row=1, col=1)

    # Naked eye and binocular limits
    fig.add_hline(y=6.5,  line_dash="dash", line_color="white",
                  annotation_text="Naked eye", row=1, col=1)
    fig.add_hline(y=10,   line_dash="dash", line_color="cyan",
                  annotation_text="Binoculars", row=1, col=1)
    fig.add_hline(y=14,   line_dash="dash", line_color="yellow",
                  annotation_text="Amateur telescope", row=1, col=1)
    fig.add_hline(y=20,   line_dash="dash", line_color="orange",
                  annotation_text="Large amateur", row=1, col=1)
    fig.add_hline(y=24.5, line_dash="dash", line_color="red",
                  annotation_text="Rubin Observatory", row=1, col=1)
    fig.add_hline(y=28,   line_dash="dash", line_color="hotpink",
                  annotation_text="VLT / Keck", row=1, col=1)

    fig.update_yaxes(autorange="reversed", row=1, col=1)  # brighter = lower number = top

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["elong"],
        line=dict(color="orange"),
        showlegend=False
    ), row=2, col=1)

    fig.add_hrect(y0=0, y1=30, fillcolor="red", opacity=0.2,
                  line_width=0, annotation_text="Too close to Sun",
                  row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df_eph["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S"),
        y=df_eph["observable"],
        fill="tozeroy",
        line=dict(color="green"),
        showlegend=False
    ), row=3, col=1)

    fig.update_layout(
        title="3I/ATLAS — When Can We Observe It?",
        height=900,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )
    fig.show()