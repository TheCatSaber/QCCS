from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)


def complex_matrix_eigenvalues(m: ComplexMatrix) -> list[ComplexNumber]:
    """Calculate the eigenvalues of a square 2 by 2 matrix,
    or a square diagonal matrix.
    """
    if not m.is_square():
        raise ValueError("Matrix for eigenvalues must be square.")

    size = m.get_width()

    if not (size == 2 or m.is_diagonal()):
        raise ValueError("Matrix for eigenvalues must be 2 by 2, or diagonal.")

    if m.is_diagonal():
        eigenvalues: list[ComplexNumber] = []
        for i in range(size):
            eigenvalues.append(m.get_row(i)[i])

        return [m.get_row(i)[i] for i in range(size)]

    a = m.get_row(0)[0]
    b = m.get_row(0)[1]
    c = m.get_row(1)[0]
    d = m.get_row(1)[1]
    trace = a + d
    determinant = (a * d) - (b * c)
    square_root = ((trace * trace) - (4 * determinant)).square_root()
    lambda1 = (trace + square_root) / 2
    lambda2 = (trace - square_root) / 2
    return [lambda1, lambda2]


def complex_matrix_eigenvectors(m: ComplexMatrix) -> list[ComplexVector]:
    """Calculate the eigenvectors of a square 2 by 2 matrix,
    or a square diagonal matrix.
    """
    if not m.is_square():
        raise ValueError("Matrix for eigenvectors must be square.")

    size = m.get_width()

    if not (size == 2 or m.is_diagonal()):
        raise ValueError("Matrix for eigenvectors must be 2 by 2, or diagonal.")

    if m.is_diagonal():
        eigenvectors: list[ComplexVector] = []
        for i in range(size):
            v = [zero for _ in range(size)]
            v[i] = one
            eigenvectors.append(ComplexVector(v))
        return eigenvectors

    eigenvalues = complex_matrix_eigenvalues(m)
    m1 = m + (eigenvalues[0].inverse() * ComplexMatrix.identity(2))
    m2 = m + (eigenvalues[1].inverse() * ComplexMatrix.identity(2))
    # Find smallest of pair
    eigenvectors: list[ComplexVector] = []
    column_0 = m2.get_column(0)
    column_1 = m2.get_column(1)
    if column_0[0].modulus() < column_1[0].modulus():
        eigenvectors.append(ComplexVector(column_0))
    else:
        eigenvectors.append(ComplexVector(column_1))

    column_0 = m1.get_column(0)
    column_1 = m1.get_column(1)
    if column_0[0].modulus() < column_1[0].modulus():
        eigenvectors.append(ComplexVector(column_0))
    else:
        eigenvectors.append(ComplexVector(column_1))

    return eigenvectors
