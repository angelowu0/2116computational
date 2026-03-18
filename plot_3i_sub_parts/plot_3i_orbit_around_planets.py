import plotly.graph_objects as go
from utils.utils import get_vectors

def plot_3i_orbit_around_planets():
    fig_3d = go.Figure()  # new figure for each planet

    # Comet trajectory
    df_comet = get_vectors(f"3I", "2025-04-01", "2026-06-01", "1d")
    fig_3d.add_trace(go.Scatter3d(
        x=df_comet["x"],
        y=df_comet["y"],
        z=df_comet["z"],
        mode="lines",
        line=dict(
            color=df_comet["v_kms"],
            colorscale="Plasma",
            width=4
        ),
        text=df_comet["datetime_str"],
        name="3I/ATLAS"
    ))

    # Sun
    fig_3d.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers",
        marker=dict(size=8, color="yellow"),
        name="Sun"
    ))

    for name, pid, colour in [
        ("Earth",   "399", "skyblue"),
        ("Mars", "499", "brown"),
        ("Jupiter", "599", "orange"),
        ("Saturn",  "699", "gold"),
    ]:
        # This planet's orbit ring
        df_orbit = get_vectors(pid, "2025-04-01", "2026-06-01", "1d", id_type="majorbody")
        fig_3d.add_trace(go.Scatter3d(
            x=df_orbit["x"],
            y=df_orbit["y"],
            z=df_orbit["z"],
            mode="lines",
            line=dict(color=colour, width=20),
            name=f"{name} orbit"
        ))

    fig_3d.update_layout(
        scene=dict(
            aspectmode="data"  # scales all three axes to match the data
        )
    )

    fig_3d.update_layout(
        title=f"3I/ATLAS — Trajectory Near Planets",
        height=700,
        scene=dict(
            xaxis_title="X (AU)",
            yaxis_title="Y (AU)",
            zaxis_title="Z (AU)",
            bgcolor="black"
        ),
        paper_bgcolor="black",
        font=dict(color="white")
    )

    fig_3d.show()