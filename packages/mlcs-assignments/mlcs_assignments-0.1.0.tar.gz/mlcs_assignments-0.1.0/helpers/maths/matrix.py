from dataclasses import dataclass, field
from helpers.maths.types import Matrix

import numpy as np


# TODO: Untested!
@dataclass(frozen=True)
class MatrixPowers:
    A: Matrix
    cache: dict[int, Matrix] = field(default_factory=dict, init=False)

    def power(self, k: int) -> Matrix:
        if k not in self.cache:
            self.cache[k] = np.linalg.matrix_power(self.A, k)

        return self.cache[k]
