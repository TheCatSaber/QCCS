from .complex_numbers import ComplexNumber


def complex_number_add(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
    return ComplexNumber(
        c1.get_real() + c2.get_real(), c1.get_imaginary() + c2.get_imaginary()
    )


def complex_number_subtract(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
    return ComplexNumber(
        c1.get_real() - c2.get_real(), c1.get_imaginary() - c2.get_imaginary()
    )


def complex_number_multiply(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
    new_real: float = (c1.get_real() * c2.get_real()) - (
        c1.get_imaginary() * c2.get_imaginary()
    )
    new_imaginary: float = (c1.get_imaginary() * c2.get_real()) + (
        c1.get_real() * c2.get_imaginary()
    )
    return ComplexNumber(new_real, new_imaginary)


def complex_number_divide(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
    modulus_squared = c2.modulus_squared()
    if modulus_squared == 0:
        raise ValueError("c2 cannot have a modulus_squared of 0.")
    new_real: float = (
        (c1.get_real() * c2.get_real()) + (c1.get_imaginary() * c2.get_imaginary())
    ) / modulus_squared
    new_imaginary: float = (
        (c2.get_real() * c1.get_imaginary()) - (c1.get_real() * c2.get_imaginary())
    ) / modulus_squared
    return ComplexNumber(new_real, new_imaginary)
