from __future__ import annotations

import math
from typing import Sequence

from complex_numbers import ComplexNumber


class ComplexVector:
    _vector: list[ComplexNumber]

    def __init__(self, complex_values: Sequence[ComplexNumber | float | int]) -> None:
        self._vector = [
            ComplexNumber(c, 0) if isinstance(c, int) or isinstance(c, float) else c
            for c in complex_values
        ]

    def __getitem__(self, n: int) -> ComplexNumber:
        return self._vector[n]

    def __len__(self) -> int:
        return len(self._vector)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComplexVector | list):
            return False
        if len(self) != len(other):  # type: ignore
            return False

        for c1, c2 in zip(self, other):  # type: ignore
            if c1 != c2:
                return False

        return True

    def inverse(self) -> ComplexVector:
        return ComplexVector([c.inverse() for c in self._vector])

    def norm(self) -> float:
        return math.sqrt(self.norm_squared())

    def norm_squared(self) -> float:
        return sum(c.modulus_squared() for c in self)

    def __add__(self, other: object) -> ComplexVector:
        if isinstance(other, ComplexVector):
            # To tell type checking that I don't care what
            # other is, since + will take care of this.
            if len(self) != len(other):
                raise ValueError("You can only add ComplexVectors of the same length.")
            return ComplexVector([self[i] + other[i] for i in range(len(self))])
        elif isinstance(other, list):
            if not all(isinstance(c, ComplexNumber | int | float) for c in other):  # type: ignore
                return NotImplemented
            return self + ComplexVector(other)  # type: ignore
        else:
            return NotImplemented

    def __radd__(self, other: object) -> ComplexVector:
        return self + other

    def __sub__(self, other: object) -> ComplexVector:
        if isinstance(other, ComplexVector):
            return self + other.inverse()
        elif isinstance(other, list):
            if not all(isinstance(c, ComplexNumber | int | float) for c in other):  # type: ignore
                return NotImplemented
            return self - ComplexVector(other)  # type: ignore
        else:
            return NotImplemented

    def __rsub__(self, other: object) -> ComplexVector:
        return self.inverse() + other

    def __rmul__(self, other: object) -> ComplexVector:
        """Left multiplication by a scalar. The matrix is on the right of the scalar."""
        if isinstance(other, ComplexNumber | int | float):
            return ComplexVector([(c * other) for c in self._vector])
        else:
            return NotImplemented
