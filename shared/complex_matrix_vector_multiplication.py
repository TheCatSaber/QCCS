from complex_matrices import ComplexMatrix, complex_matrix_multiply
from complex_vectors import ComplexVector


def complex_matrix_vector_multiply(m: ComplexMatrix, v: ComplexVector) -> ComplexVector:
    # Turn v into a matrix, and use complex_matrix_multiply.
    m2 = ComplexMatrix([[i] for i in v])
    result = complex_matrix_multiply(m, m2)
    result_height = result.get_height()
    return ComplexVector([result.get_row(i)[0] for i in range(result_height)])
