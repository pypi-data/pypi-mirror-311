import sympy as sp
from sympy import latex
from helpers.maths.types import Matrix, Vector

import numpy as np


def pretty_matrix(matrix: Matrix, limit: int) -> str:
    vdots, cdots, ddots = sp.symbols(r"\vdots \cdots \ddots")
    m, n = matrix.shape
    rounded = np.round(matrix, 3)
    symbolic = sp.Matrix(rounded[:limit, :limit])

    if m > limit:
        columns = symbolic.shape[1]
        symbolic = symbolic.row_insert(  # This inserts a row of vertical dots
            limit,
            sp.Matrix([[vdots for _ in range(columns)]]),
        )
        symbolic = symbolic.row_insert(  # This inserts the last row
            limit + 1,
            sp.Matrix([[rounded[-1, j] for j in range(columns)]]),
        )

    if n > limit:
        rows = symbolic.shape[0]
        symbolic = symbolic.col_insert(  # This inserts a column of horizontal dots
            limit,
            sp.Matrix([cdots for _ in range(rows)]),
        )
        symbolic = symbolic.col_insert(  # This inserts the last column
            limit + 1,
            sp.Matrix([rounded[i, -1] for i in range(rows)]),
        )

    if m > limit and n > limit:
        symbolic[limit, limit] = ddots  # This inserts a diagonal of dots
        symbolic[limit + 1, limit + 1] = rounded[-1, -1]

    return latex(symbolic)


def pretty_vector(vector: Vector, limit: int) -> str:
    vdots = sp.symbols(r"\vdots")
    (m,) = vector.shape
    rounded = np.round(vector, 3)
    symbolic = sp.Matrix(rounded[:limit])

    if m > limit:
        symbolic = symbolic.row_insert(limit, sp.Matrix([vdots]))
        symbolic = symbolic.row_insert(limit + 1, sp.Matrix([rounded[-1]]))

    return latex(symbolic)


def pretty_latex(value: Vector | Matrix, limit: int = 5) -> str:
    return (
        pretty_vector(value, limit) if value.ndim == 1 else pretty_matrix(value, limit)
    )
