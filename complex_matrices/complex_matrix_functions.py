from complex_numbers import ComplexNumber, complex_number_add, complex_number_multiply

from complex_matrices import ComplexMatrix


def complex_matrix_add(m1: ComplexMatrix, m2: ComplexMatrix) -> ComplexMatrix:
    if m1.get_width() != m2.get_width():
        raise ValueError("m1 and m2 have different widths.")
    if m1.get_height() != m2.get_height():
        raise ValueError("m1 and m2 are of different sizes.")
    new_matrix: list[list[ComplexNumber]] = []
    for row_index in range(m1.get_height()):
        new_matrix.append(
            [
                complex_number_add(i1, i2)
                for i1, i2 in zip(m1.get_row(row_index), m2.get_row(row_index))
            ]
        )
    return ComplexMatrix(new_matrix)


def complex_matrix_multiply(m1: ComplexMatrix, m2: ComplexMatrix) -> ComplexMatrix:
    """Multiply an m x n matrix by a n x p matrix, to produce a m x p matrix.

    Raises ValueError if sizes are not correct.
    """
    m = m1.get_height()
    n1 = m1.get_width()  # n according to m1
    n2 = m2.get_height()  # n according to m2
    p = m2.get_width()

    if n1 != n2:
        raise ValueError(
            f"Cannot multiply matrices due to incorrect sizes: width of first {n1} is"
            f" not equal to height of second {n2}"
        )
    n = n1  # Just to make naming clearer.
    new_matrix: list[list[ComplexNumber]] = []
    # (m1 x m2)[j, k] = sum from h = 0 to h = n-1 of A[j, h] * B[h, k]
    for j in range(m):
        new_row: list[ComplexNumber] = []
        for k in range(p):
            sum_ = ComplexNumber(0, 0)
            for h in range(n):
                multiplication = complex_number_multiply(
                    m1.get_row(j)[h], m2.get_row(h)[k]
                )
                sum_ = complex_number_add(sum_, multiplication)
            new_row.append(sum_)
        new_matrix.append(new_row)
    return ComplexMatrix(new_matrix)
