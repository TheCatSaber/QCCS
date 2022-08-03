from __future__ import annotations

import math

from complex_numbers import ComplexNumber, complex_number_multiply


class ComplexVector:
    _vector: list[ComplexNumber]

    def __init__(self, complex_values: list[ComplexNumber]) -> None:
        self._vector = complex_values

    def __getitem__(self, n: int) -> ComplexNumber:
        return self._vector[n]

    def __len__(self) -> int:
        return len(self._vector)

    def __eq__(self, other: object) -> bool:
        if type(other) not in [type(self), list]:
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
        return ComplexVector([complex_number_multiply(c, scalar) for c in self._vector])

    def norm(self) -> float:
        return math.sqrt(self.norm_squared())

    def norm_squared(self) -> float:
        return sum(c.modulus_squared() for c in self)
