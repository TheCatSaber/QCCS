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

    def scalar_multiplication(self, scalar: ComplexNumber) -> ComplexVector:
        return ComplexVector([(c * scalar) for c in self._vector])

    def norm(self) -> float:
        return math.sqrt(self.norm_squared())

    def norm_squared(self) -> float:
        return sum(c.modulus_squared() for c in self)
