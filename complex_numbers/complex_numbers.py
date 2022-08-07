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
        def handle_int_str(value: float) -> str:
            if isinstance(value, int) or value.is_integer():
                return str(int(value))
            return str(value)

        re_str = handle_int_str(self._re)

        im_str = handle_int_str(self._im)

        match (self._re, self._im):
            case (_, 0):
                return re_str
            case (0, 1):
                return "i"
            case (0, -1):
                return "-i"
            case (0, _):
                return im_str + "i"
            case _:
                sign = "-" if self._im < 0 else "+"
                im_str = im_str.replace("-", "")
                return f"{re_str} {sign} {im_str}i"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int | float):
            return self.is_real() and math.isclose(self._re, other, abs_tol=1e-8)

        if isinstance(other, ComplexNumber):
            return math.isclose(self._re, other._re, abs_tol=1e-8) and math.isclose(
                self._im, other._im, abs_tol=1e-8
            )
        else:
            return False

    def modulus(self) -> float:
        return math.sqrt(self.modulus_squared())

    def modulus_squared(self) -> float:
        return (self._re * self._re) + (self._im * self._im)

    def conjugate(self) -> ComplexNumber:
        return ComplexNumber(self._re, -self._im)

    def to_polar(self) -> tuple[float, float]:
        r = self.modulus()
        theta = math.atan2(self._im, self._re)
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

    def is_non_negative_real(self) -> bool:
        return self._re >= 0 and self.is_real()

    def is_integer(self) -> bool:
        return (isinstance(self._re, int) or self._re.is_integer()) and self.is_real()

    def is_positive_integer(self) -> bool:
        return self.is_positive_real() and self.is_integer()

    def is_non_negative_integer(self) -> bool:
        return self.is_non_negative_real() and self.is_integer()

    def square_root(self) -> ComplexNumber:
        r, theta = self.to_polar()
        return self.new_from_polar(math.sqrt(r), theta / 2)

    def __add__(self, other: object) -> ComplexNumber:
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self._re + other._re, self._im + other._im)
        elif isinstance(other, int | float):
            return ComplexNumber(self._re + other, self._im)
        else:
            raise NotImplementedError

    def __radd__(self, other: object) -> ComplexNumber:
        return self + other

    def __sub__(self, other: object) -> ComplexNumber:
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self._re - other._re, self._im - other._im)
        elif isinstance(other, int | float):
            return ComplexNumber(self._re - other, self._im)
        else:
            raise NotImplementedError

    def __rsub__(self, other: object) -> ComplexNumber:
        if isinstance(other, ComplexNumber | int | float):
            return other + self.inverse()
        else:
            raise NotImplementedError

    def __mul__(self, other: object) -> ComplexNumber:
        if isinstance(other, int | float):
            return ComplexNumber(self._re * other, self._im * other)
        elif isinstance(other, ComplexNumber):
            new_real: float = (self._re * other._re) - (self._im * other._im)
            new_imaginary: float = (self._im * other._re) + (self._re * other._im)
            return ComplexNumber(new_real, new_imaginary)
        else:
            raise NotImplementedError

    def __rmul__(self, other: object) -> ComplexNumber:
        return self * other

    def __truediv__(self, other: object) -> ComplexNumber:
        if isinstance(other, int | float):
            return ComplexNumber(self._re / other, self._im / other)
        if not isinstance(other, ComplexNumber):
            raise NotImplementedError
        modulus_squared = other.modulus_squared()
        return (self * other.conjugate()) / modulus_squared

    def __rtruediv__(self, other: object) -> ComplexNumber:
        if isinstance(other, int | float):
            return (other * self.conjugate()) / self.modulus_squared()
        # other should never ComplexNumber
        else:
            raise NotImplementedError
