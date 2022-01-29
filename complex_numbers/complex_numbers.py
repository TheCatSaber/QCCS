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
        else:
            return self.get_real() == other.get_real() and self.get_imaginary() == other.get_imaginary()  # type: ignore

    @staticmethod
    def modulus(c: ComplexNumber) -> float:
        return math.sqrt(ComplexNumber.modulus_squared(c))

    @staticmethod
    def modulus_squared(c: ComplexNumber) -> float:
        return (c._re * c._re) + (c._im * c._im)

    @staticmethod
    def conjugate(c: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(c._re, -c._im)

    @staticmethod
    def add(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(c1._re + c2._re, c1._im + c2._im)

    @staticmethod
    def subtract(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(c1._re - c2._re, c1._im - c2._im)

    @staticmethod
    def multiply(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        new_real: float = (c1._re * c2._re) - (c1._im * c2._im)
        new_imaginary: float = (c1._im * c2._re) + (c1._re * c2._im)
        return ComplexNumber(new_real, new_imaginary)

    @staticmethod
    def divide(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        modulus_squared = ComplexNumber.modulus_squared(c2)
        if modulus_squared == 0:
            raise ValueError("c2 cannot have a modulus_squared of 0.")
        new_real: float = ((c1._re * c2._re) + (c1._im * c2._im)) / modulus_squared
        new_imaginary: float = ((c2._re * c1._im) - (c1._re * c2._im)) / modulus_squared
        return ComplexNumber(new_real, new_imaginary)

    def to_polar(self) -> tuple[float, float]:
        r = self.modulus(self)
        theta = math.atan2(self._re, self._im)
        return r, theta
    
    @staticmethod
    def from_polar(r: float, theta: float) -> ComplexNumber:
        return ComplexNumber(r * math.cos(theta), r * math.sin(theta))