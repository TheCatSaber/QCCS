from .complex_vectors import ComplexVector
from complex_numbers import complex_number_add


def complex_vector_add(v1: ComplexVector, v2: ComplexVector) -> ComplexVector:
    if len(v1) != len(v2):
        raise ValueError("You can only add ComplexVectors of the same length.")
    return ComplexVector([complex_number_add(v1[i], v2[i]) for i in range(len(v1))])
