from __future__ import annotations

import math


class ComplexNumber:
    _re: float
    _im: float

    def __init__(self, real: float, imaginary: float) -> None:
        self._re = real
        self._im = imaginary

    def get_real(self) -> float:
        return self._re

    def get_imaginary(self) -> float:
        return self._im

    def __str__(self) -> str:
        sign = "+"
        if self._im < 0:
            sign = "-"
        return f"{self._re} {sign} {abs(self._im)}i"

    def __eq__(self, other: object) -> bool:
        if type(other) != type(self):
            return False
        return math.isclose(self.get_real(), other.get_real(), abs_tol=1e-8) and math.isclose(self.get_imaginary(), other.get_imaginary(), abs_tol=1e-8)  # type: ignore

    def modulus(self) -> float:
        return math.sqrt(self.modulus_squared())

    def modulus_squared(self) -> float:
        return (self._re * self._re) + (self._im * self._im)

    def conjugate(self) -> ComplexNumber:
        return ComplexNumber(self._re, -self._im)

    def to_polar(self) -> tuple[float, float]:
        r = self.modulus()
        theta = math.atan2(self._re, self._im)
        return r, theta

    @staticmethod
    def new_from_polar(r: float, theta: float) -> ComplexNumber:
        return ComplexNumber(r * math.cos(theta), r * math.sin(theta))

    def inverse(self) -> ComplexNumber:
        return ComplexNumber(-self._re, -self._im)

    def is_real(self) -> bool:
        return self._im == 0

    def is_positive_real(self) -> bool:
        return self._re > 0 and self.is_real()

    def is_integer(self) -> bool:
        return (type(self._re) == int or self._re.is_integer()) and self.is_real()

    def is_positive_integer(self) -> bool:
        return self.is_positive_real() and self.is_integer()
