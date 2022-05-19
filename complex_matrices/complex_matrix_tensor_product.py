from typing import Optional

from complex_numbers import ComplexNumber, complex_number_multiply

from .complex_matrices import ComplexMatrix


def tensor_product(m1: ComplexMatrix, m2: ComplexMatrix) -> ComplexMatrix:
    m1_height = m1.get_height()
    m1_width = m1.get_width()
    m2_height = m2.get_height()
    m2_width = m2.get_width()

    resultant_height = m1_height * m2_height
    resultant_width = m1_width * m2_width
    new_matrix: list[list[Optional[ComplexNumber]]] = [
        [None for _ in range(resultant_width)] for _ in range(resultant_height)
    ]
    for row1_index in range(m1_height):
        row1 = m1.get_row(row1_index)
        for column1_index, value1 in enumerate(row1):
            for row2_index in range(m2_height):
                row2 = m2.get_row(row2_index)
                for column2_index, value2 in enumerate(row2):
                    new_matrix[row1_index * m2_height + row2_index][
                        column1_index * m2_width + column2_index
                    ] = complex_number_multiply(value1, value2)

    return ComplexMatrix(new_matrix)  # type: ignore
