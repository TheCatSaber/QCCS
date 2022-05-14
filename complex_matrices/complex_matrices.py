from __future__ import annotations

from complex_numbers import ComplexNumber, complex_number_multiply


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
