from helpers.maths import Vector
from plotly.subplots import make_subplots

import numpy as np
import plotly.graph_objects as go


def add_responses_to(
    figure: go.Figure, *, y: Vector, y_d: Vector, t: Vector, subtitle: str
) -> None:
    figure.add_trace(
        go.Scatter(x=t, y=y, mode="lines+markers", name="Actual"), row=1, col=1
    )
    figure.add_trace(
        go.Scatter(x=t, y=y_d, mode="lines+markers", name="Desired"), row=1, col=1
    )

    if subtitle:
        figure.add_trace(
            go.Scatter(
                x=[t[0]],
                y=[max(max(y), max(y_d))],
                mode="text",
                text=[subtitle],
                showlegend=False,
                textposition="top right",
            ),
            row=1,
            col=1,
        )


def add_error_to(figure: go.Figure, *, y: Vector, y_d: Vector, t: Vector) -> None:
    figure.add_trace(
        go.Scatter(
            x=t, y=y_d - y, mode="lines+markers", name="Error", line=dict(color="green")
        ),
        row=2,
        col=1,
    )


def add_traces_to(
    figure: go.Figure, *, y: Vector, y_d: Vector, t: Vector, subtitle: str
) -> None:
    add_responses_to(figure, y=y, y_d=y_d, t=t, subtitle=subtitle)
    add_error_to(figure, y=y, y_d=y_d, t=t)


def plot_responses(
    y: Vector, y_d: Vector, Δt: float, *, show: bool = True, subtitle: str = ""
) -> go.Figure:
    assert (
        y.shape == y_d.shape
    ), f"The lengths of the responses ({y.shape} and {y_d.shape}) do not match."

    t = np.arange(0, len(y_d) * Δt, Δt)
    y_max = max(max(y), max(y_d))
    error_range = [-y_max * 1.1, y_max * 1.1]

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("System Responses", "Error"),
    )

    add_traces_to(figure, y=y, y_d=y_d, t=t, subtitle=subtitle)

    figure.update_layout(
        title=f"System Responses and Error (Δt = {Δt})",
        xaxis_title="Time",
        height=700,
    )

    figure.update_yaxes(title_text="Output", row=1, col=1)
    figure.update_yaxes(title_text="Error", range=error_range, row=2, col=1)
    figure.update_xaxes(title_text="Time", row=2, col=1)

    if show:
        figure.show()

    return figure
