import math

from complex_numbers import ComplexNumber, complex_number_add, complex_number_multiply

from .complex_vectors import ComplexVector


def complex_vector_add(v1: ComplexVector, v2: ComplexVector) -> ComplexVector:
    if len(v1) != len(v2):
        raise ValueError("You can only add ComplexVectors of the same length.")
    return ComplexVector([complex_number_add(v1[i], v2[i]) for i in range(len(v1))])


def complex_vector_inner_product(v1: ComplexVector, v2: ComplexVector) -> ComplexNumber:
    if (size := len(v1)) != len(v2):
        raise ValueError(
            "You can only take the inner product of ComplexVectors of the same length."
        )
    total = ComplexNumber(0, 0)
    for i in range(size):
        multiplication = complex_number_multiply(v1[i].conjugate(), v2[i])
        total = complex_number_add(total, multiplication)
    return total


def complex_vector_norm(v: ComplexVector) -> float:
    return math.sqrt(complex_vector_inner_product(v, v).get_real())


def complex_vector_distance(v1: ComplexVector, v2: ComplexVector) -> float:
    return complex_vector_norm(complex_vector_add(v1, v2.inverse()))
