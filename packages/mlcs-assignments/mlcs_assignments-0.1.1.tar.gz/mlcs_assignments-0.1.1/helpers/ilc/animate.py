from typing import TypeAlias, Protocol, TypeVar, Generic
from numpy.typing import NDArray
from helpers.ilc.system import LiftedSystem
from helpers.ilc.plot import plot_responses
from helpers.robot import animation_configuration

import plotly.graph_objects as go
import numpy as np

Vector: TypeAlias = NDArray[np.floating]


class IterationCallback(Protocol):
    def __call__(self, iteration: int, y: Vector, y_d: Vector) -> None:
        """Called after each iteration of the ILC algorithm."""


class Disturbance(Protocol):
    def __call__(self, j: int, u: Vector) -> Vector:
        """Returns the disturbance at iteration j given the input u."""
        ...


LiftedSystemT = TypeVar("LiftedSystemT", bound=LiftedSystem, infer_variance=True)


class IlcAlgorithm(Protocol, Generic[LiftedSystemT]):
    def __call__(
        self,
        lifted_system: LiftedSystemT,
        *,
        y_d: Vector,
        u: Vector,
        v: float,
        s: float,
        r: float,
        max_iterations: int,
        on_iteration: IterationCallback,
    ) -> Vector:
        """Runs the ILC algorithm on the given system."""
        ...


def animated_ilc_frames(
    lifted_system: LiftedSystemT,
    ilc: IlcAlgorithm[LiftedSystemT],
    *,
    y_d: Vector,
    u: Vector,
    v: float,
    s: float,
    r: float,
    max_iterations: int,
    Δt: float,
) -> list[go.Figure]:
    frames: list[go.Figure] = []

    def create_frame(iteration: int, y: Vector, y_d: Vector) -> None:
        frames.append(
            plot_responses(y, y_d, Δt=Δt, subtitle=f"Iteration {iteration}", show=False)
        )

    u = ilc(
        lifted_system,
        y_d=y_d,
        u=u,
        v=v,
        s=s,
        r=r,
        max_iterations=max_iterations,
        on_iteration=create_frame,
    )

    return frames


def animate_ilc(
    lifted_system: LiftedSystem,
    ilc: IlcAlgorithm,
    *,
    y_d: Vector,
    u: Vector,
    v: float,
    s: float,
    r: float,
    max_iterations: int,
    Δt: float,
) -> None:
    frames: list[go.Figure] = animated_ilc_frames(
        lifted_system,
        ilc,
        y_d=y_d,
        u=u,
        v=v,
        s=s,
        r=r,
        max_iterations=max_iterations,
        Δt=Δt,
    )

    figure = go.Figure(
        data=frames[0].data,
        layout=frames[0].layout,
        frames=[go.Frame(data=figure.data) for figure in frames],
    )

    figure.update_layout(updatemenus=[animation_configuration()])
    figure.show()


def no_callback(iteration: int, y: Vector, y_d: Vector) -> None:
    pass


def no_disturbance(j: int, u: Vector) -> Vector:
    return np.zeros(u.shape)
