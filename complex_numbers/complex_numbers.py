from __future__ import annotations


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
    def add(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(c1._re + c2._re, c1._im + c2._im)

    @staticmethod
    def multiply(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        new_real: float = (c1._re * c2._re) - (c1._im * c2._im)
        new_imaginary: float = (c1._im * c2._re) + (c1._re * c2._im)
        return ComplexNumber(new_real, new_imaginary)