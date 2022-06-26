from __future__ import annotations

from complex_numbers import ComplexNumber, complex_number_add, complex_number_multiply


class ComplexMatrix:
    _matrix: list[list[ComplexNumber]]

    def __init__(self, matrix: list[list[ComplexNumber]]) -> None:
        """Each inner list is a row.
        Each column is the elements in each row with the same index.
        """
        try:
            first_length = len(matrix[0])
        except IndexError:  # this means they passed [] as a list
            raise TypeError(
                "ComplexMatrix called with empty list (== []) as the matrix."
            )
        if first_length == 0:  # this means there is nothing in the items
            raise ValueError("Cannot call ComplexMatrix with lists of length 0.")
        for row in matrix:
            if len(row) != first_length:
                raise ValueError(
                    "matrix passed to ComplexMatrix must have rows of consistent"
                    " lengths."
                )
        self._matrix = matrix

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        if self.get_width() != __o.get_width() or self.get_height() != __o.get_height():  # type: ignore
            return False
        for row_index in range(self.get_height()):
            if self.get_row(row_index) != __o.get_row(row_index):  # type: ignore
                return False

        return True

    def get_width(self):
        """Get length of a row."""
        return len(self._matrix[0])

    def get_height(self):
        """Get height of a column."""
        return len(self._matrix)

    def get_row(self, i: int) -> list[ComplexNumber]:
        if i < 0 or i >= self.get_height():  # equal to get_height because of 0 indexing
            raise ValueError("Invalid index.")
        return self._matrix[i]

    def inverse(self) -> ComplexMatrix:
        new_matrix: list[list[ComplexNumber]] = []
        for row_index in range(self.get_height()):
            new_matrix.append([i.inverse() for i in self.get_row(row_index)])
        return ComplexMatrix(new_matrix)

    def scalar_multiplication(self, scalar: ComplexNumber) -> ComplexMatrix:
        new_matrix: list[list[ComplexNumber]] = []
        for row_index in range(self.get_height()):
            new_matrix.append(
                [complex_number_multiply(i, scalar) for i in self.get_row(row_index)]
            )
        return ComplexMatrix(new_matrix)

    def conjugate(self) -> ComplexMatrix:
        new_matrix: list[list[ComplexNumber]] = []
        for row_index in range(self.get_height()):
            new_matrix.append([i.conjugate() for i in self.get_row(row_index)])
        return ComplexMatrix(new_matrix)

    def transpose(self) -> ComplexMatrix:
        new_matrix: list[list[ComplexNumber]] = []
        for column_index in range(self.get_width()):
            new_row: list[ComplexNumber] = []
            for row_index in range(self.get_height()):
                new_row.append(self.get_row(row_index)[column_index])
            new_matrix.append(new_row)
        return ComplexMatrix(new_matrix)

    def adjoint(self) -> ComplexMatrix:
        return self.transpose().conjugate()

    def is_hermitian(self) -> bool:
        return self == self.adjoint()

    def is_unitary(self) -> bool:
        self_times_adjoint = complex_matrix_multiply(self, self.adjoint())
        return self_times_adjoint == identity(self_times_adjoint.get_width())

    def is_square(self) -> bool:
        return self.get_width() == self.get_height()


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


def identity(n: int) -> ComplexMatrix:
    if n <= 0:
        raise ValueError("Identity size must be a positive integer.")
    matrix: list[list[ComplexNumber]] = []
    for i in range(n):
        row: list[ComplexNumber] = []
        for j in range(n):
            if i == j:  # Element on the diagonal
                row.append(ComplexNumber(1, 0))
            else:
                row.append(ComplexNumber(0, 0))
        matrix.append(row)
    return ComplexMatrix(matrix)
