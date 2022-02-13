from complex_numbers import ComplexNumber, complex_number_add

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
