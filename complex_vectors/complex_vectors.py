from __future__ import annotations

from complex_numbers import ComplexNumber


class ComplexVector:
    _vector: list[ComplexNumber]

    def __init__(self, complex_values: list[ComplexNumber]) -> None:
        self._vector = complex_values

    def __getitem__(self, n: int) -> ComplexNumber:
        return self._vector[n]

    def __len__(self) -> int:
        return len(self._vector)

    def __eq__(self, other: object) -> bool:
        if type(other) != type(self):
            return False
        if len(self) != len(other):  # type: ignore
            return False

        for c1, c2 in zip(self, other):  # type: ignore
            if c1 != c2:
                return False

        return True

    @staticmethod
    def add(v1: ComplexVector, v2: ComplexVector) -> ComplexVector:
        if len(v1) != len(v2):
            raise ValueError("You can only add ComplexVectors of the same length.")
        return ComplexVector(
            [ComplexNumber.add(v1[i], v2[i]) for i in range(len(v1))]
        )

    def inverse(self) -> ComplexVector:
        return ComplexVector([c.inverse() for c in self._vector])

    def scalar_multiplication(self, scalar: ComplexNumber) -> ComplexVector:
        return ComplexVector(
            [ComplexNumber.multiply(c, scalar) for c in self._vector]
        )
