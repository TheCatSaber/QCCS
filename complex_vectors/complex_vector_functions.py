from complex_numbers import ComplexNumber

from .complex_vectors import ComplexVector


def complex_vector_add(v1: ComplexVector, v2: ComplexVector) -> ComplexVector:
    if len(v1) != len(v2):
        raise ValueError("You can only add ComplexVectors of the same length.")
    return ComplexVector([v1[i] + v2[i] for i in range(len(v1))])


def complex_vector_inner_product(v1: ComplexVector, v2: ComplexVector) -> ComplexNumber:
    if (size := len(v1)) != len(v2):
        raise ValueError(
            "You can only take the inner product of ComplexVectors of the same length."
        )
    total = ComplexNumber(0, 0)
    for i in range(size):
        total += v1[i].conjugate() * v2[i]
    return total


def complex_vector_distance(v1: ComplexVector, v2: ComplexVector) -> float:
    return complex_vector_add(v1, v2.inverse()).norm()


def complex_vector_tensor_product(
    v1: ComplexVector, v2: ComplexVector
) -> ComplexVector:
    return ComplexVector([c1 * c2 for c1 in v1 for c2 in v2])
