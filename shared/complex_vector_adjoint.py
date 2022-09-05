from complex_matrices import ComplexMatrix
from complex_vectors import ComplexVector


def complex_vector_adjoint(v: ComplexVector) -> ComplexMatrix:
    return ComplexMatrix([[i.conjugate()] for i in v])
