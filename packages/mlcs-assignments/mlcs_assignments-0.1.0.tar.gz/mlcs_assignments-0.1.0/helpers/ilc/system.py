from typing import Protocol
from helpers.maths import Matrix, Vector, pretty_latex
from IPython.display import display, Math

import numpy as np


class LiftedSystem(Protocol):
    def response(self, u: Vector, v: Vector) -> Vector:
        """Returns the response of the lifted system to the input u and disturbance v."""
        ...

    @property
    def m(self) -> int:
        """Returns the shift between the input and output of the system."""
        ...

    @property
    def G(self) -> Matrix:
        """Returns the matrix G of the lifted system."""
        ...

    @property
    def y_0(self) -> Vector:
        """Returns the initial output of the lifted system."""
        ...


# TODO: Untested!
class LiftedSystemMixin:
    def response_to(
        self: LiftedSystem, u: Vector, v: Vector | None = None, shift: bool = False
    ) -> Vector:
        # No disturbance is the same as a zero vector
        v = np.zeros(u.shape) if v is None else v

        # The shift here comes in handy when comparing the lifted system response to
        # the manually calculated impulse response.
        return np.concat((np.zeros(self.m if shift else 0), self.response(u, v)))

    def display(self: LiftedSystem) -> None:
        display(
            Math(
                rf"m = {self.m},\quad"
                rf"\mathbf{{G}} = {pretty_latex(self.G)},\quad"
                rf"\mathbf{{y_0}} = {pretty_latex(self.y_0)}"
            )
        )

    @property
    def N(self: LiftedSystem) -> int:
        return self.G.shape[0]


# TODO: Untested!
def impulse(N: int) -> Vector:
    assert N > 0, "The size of the impulse response must be greater than 0."

    impulse = np.zeros(N)
    impulse[0] = 1

    return impulse


# TODO: Untested!
def system_matrices_for(
    *, Δt: float, J: float, B: float
) -> tuple[Matrix, Vector, Vector]:
    A = np.array([[1, Δt], [0, 1 - Δt * B / J]])
    b = np.array([0, Δt / J])
    c = np.array([1, 0])

    return A, b, c


# TODO: Untested!
def system_response_to(
    *, u: Vector, A: Matrix, b: Vector, c: Vector, x_0: Vector
) -> Vector:
    x = x_0
    y = []

    for u_i in u:
        y.append(c.T @ x)
        x = A @ x + b * u_i

    return np.array(y)
