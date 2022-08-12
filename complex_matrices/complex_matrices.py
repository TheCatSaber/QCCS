from __future__ import annotations

from typing import Sequence, TypeGuard

from complex_numbers import ComplexNumber

zero = ComplexNumber(0, 0)


def _is_complex_matrixable(
    m: object,
) -> TypeGuard[Sequence[Sequence[ComplexNumber | int | float]]]:
    try:
        _ = len(m)  # type: ignore
        outer_iter = iter(m)  # type: ignore
        for i in outer_iter:  # type: ignore
            _ = len(i)  # type: ignore
            inner_iter = iter(i)  # type: ignore
            for c in inner_iter:  # type: ignore
                if not isinstance(c, ComplexNumber | int | float):
                    return False
    except TypeError:
        return False
    else:
        return True


class ComplexMatrix:
    _matrix: list[list[ComplexNumber]]

    def __init__(self, matrix: Sequence[Sequence[ComplexNumber | int | float]]) -> None:
        """Each inner list is a row.
        Each column is the elements in each row with the same index.
        """
        try:
            first_length = len(matrix[0])
        except IndexError:  # empty list
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
        new_matrix: list[list[ComplexNumber]] = [
            [c if isinstance(c, ComplexNumber) else ComplexNumber(c, 0) for c in row]
            for row in matrix
        ]
        self._matrix = new_matrix

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComplexMatrix):
            if (
                self.get_width() != other.get_width()
                or self.get_height() != other.get_height()
            ):
                return False
            for row_index in range(self.get_height()):
                if self.get_row(row_index) != other.get_row(row_index):
                    return False

            return True
        elif isinstance(other, list) and all(isinstance(i, list) for i in other):  # type: ignore
            if len(other) != self.get_height():  # type: ignore
                return False
            for row_index in range(self.get_height()):
                if self.get_row(row_index) != other[row_index]:
                    return False

            return True
        else:
            return False

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

    def get_column(self, i: int) -> list[ComplexNumber]:
        if i < 0 or i >= self.get_width():  # equal to get_width because of 0 indexing
            raise ValueError("Invalid index.")
        return [row[i] for row in self._matrix]

    def inverse(self) -> ComplexMatrix:
        new_matrix: list[list[ComplexNumber]] = []
        for row_index in range(self.get_height()):
            new_matrix.append([i.inverse() for i in self.get_row(row_index)])
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
        self_times_adjoint = self * self.adjoint()
        return self_times_adjoint == self.identity(self_times_adjoint.get_width())

    def is_square(self) -> bool:
        return self.get_width() == self.get_height()

    def moduli_squared_matrix(self) -> ComplexMatrix:
        return ComplexMatrix(
            [
                [ComplexNumber(c.modulus_squared(), 0) for c in row]
                for row in self._matrix
            ]
        )

    def is_diagonal(self) -> bool:
        if not self.is_square():
            return False

        for i, row in enumerate(self._matrix):
            for j, c in enumerate(row):
                if i != j and c != zero:
                    return False

        return True

    def __add__(self, other: object) -> ComplexMatrix:
        if isinstance(other, ComplexMatrix):
            if (
                self.get_width() != other.get_width()
                or self.get_height() != other.get_height()
            ):
                raise ValueError("Cannot add matrices of different sizes.")
            new_matrix: list[list[ComplexNumber]] = []
            for row_index in range(self.get_height()):
                new_matrix.append(
                    [
                        i1 + i2
                        for i1, i2 in zip(
                            self.get_row(row_index), other.get_row(row_index)
                        )
                    ]
                )
            return ComplexMatrix(new_matrix)
        elif _is_complex_matrixable(other):
            return self + ComplexMatrix(other)
        return NotImplemented

    def __radd__(self, other: object) -> ComplexMatrix:
        return self + other

    def __mul__(
        self, other: object
    ) -> ComplexMatrix:  # | list[ComplexNumber | int | float]:
        """Multiply an m x n matrix by a n x p matrix, to produce a m x p matrix.

        Raises ValueError if sizes are not correct.
        """
        if isinstance(other, ComplexMatrix):
            m = self.get_height()
            n1 = self.get_width()  # n according to self
            n2 = other.get_height()  # n according to other
            p = other.get_width()

            if n1 != n2:
                raise ValueError(
                    "Cannot multiply matrices due to incorrect sizes: width of first"
                    f" {n1} is not equal to height of second {n2}"
                )
            n = n1  # Just to make naming clearer.
            new_matrix: list[list[ComplexNumber]] = []
            # (m1 x m2)[j, k] = sum from h = 0 to h = n-1 of A[j, h] * B[h, k]
            for j in range(m):
                new_row: list[ComplexNumber] = []
                for k in range(p):
                    sum_ = ComplexNumber(0, 0)
                    for h in range(n):
                        sum_ += self.get_row(j)[h] * other.get_row(h)[k]
                    new_row.append(sum_)
                new_matrix.append(new_row)
            return ComplexMatrix(new_matrix)
        elif _is_complex_matrixable(other):
            return self * ComplexMatrix(other)
        else:
            return NotImplemented

    def __rmul__(self, other: object) -> ComplexMatrix:
        if isinstance(other, ComplexNumber | int | float):
            new_matrix: list[list[ComplexNumber]] = []
            for row_index in range(self.get_height()):
                new_matrix.append([(i * other) for i in self.get_row(row_index)])
            return ComplexMatrix(new_matrix)
        elif _is_complex_matrixable(other):
            return ComplexMatrix(other) * self
        else:
            return NotImplemented

    @classmethod
    def identity(cls, n: int) -> ComplexMatrix:
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
        return cls(matrix)
