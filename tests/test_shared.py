import unittest

import math

from context import (
    ComplexMatrix,
    ComplexNumber,
    ComplexVector,
    complex_matrix_eigenvalues,
    complex_matrix_eigenvectors,
    complex_matrix_vector_multiply,
    complex_vector_adjoint,
    normalized_complex_matrix_eigenvectors,
)

v2 = ComplexVector([ComplexNumber(2, 1), ComplexNumber(1, 1)])
i2 = ComplexMatrix([[1, 0], [0, 1]])
rotation_90_2D = ComplexMatrix([[0, -1], [1, 0]])

m5x5 = ComplexMatrix(
    [
        [1] + [0] * 4,
        [0, 3] + [0] * 3,
        [0] * 2 + [4] + [0] * 2,
        [0] * 3 + [-1, 0],
        [0] * 4 + [-2],
    ]
)


class ComplexMatrixVectorMultiplicationCheck(unittest.TestCase):
    def test_2_by_2_identity(self):
        self.assertEqual(complex_matrix_vector_multiply(i2, v2), v2)

    def test_2_by_2_rotation(self):
        self.assertEqual(
            complex_matrix_vector_multiply(rotation_90_2D, v2),
            ComplexVector([ComplexNumber(-1, -1), ComplexNumber(2, 1)]),
        )


class ComplexMatrixEigenvaluesCheck(unittest.TestCase):
    def test_not_square(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvalues(ComplexMatrix([[1, 1], [3, 3], [4, 4]]))

    def test_not_diagonal_or_two_by_two(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvalues(
                ComplexMatrix([[1, 1, 0], [0, 1, 0], [0, 0, -1]])
            )

    def test_2_by_2(self):
        self.assertEqual(
            complex_matrix_eigenvalues(ComplexMatrix([[4, 3], [-2, -3]])),
            [3, -2],
        )

    def test_large_diagonal(self):
        self.assertEqual(
            complex_matrix_eigenvalues(m5x5),
            [1, 3, 4, -1, -2],
        )


class ComplexMatrixEigenvectorsCheck(unittest.TestCase):
    def test_not_square(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvectors(
                ComplexMatrix([[1, 1], [3, 3], [4, 4]]),
            )

    def test_not_diagonal_or_two_by_two(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvectors(
                ComplexMatrix([[1, 1, 0], [0, 1, 0], [0, 0, -1]]),
            )

    def test_2_by_2(self):
        self.assertEqual(
            complex_matrix_eigenvectors(ComplexMatrix([[4, 3], [-2, -3]])),
            [
                ComplexVector([3, -1]),
                ComplexVector([1, -2]),
            ],
        )

    def test_another_2_by_2_for_ordering(self):
        self.assertEqual(
            complex_matrix_eigenvectors(ComplexMatrix([[-1, 2], [1, 0]])),
            [ComplexVector([1, 1]), ComplexVector([2, -1])],
        )

    def test_large_diagonal(self):
        self.assertEqual(
            complex_matrix_eigenvectors(m5x5),
            [
                ComplexVector([1] + [0] * 4),
                ComplexVector([0, 1] + [0] * 3),
                ComplexVector([0] * 2 + [1] + [0] * 2),
                ComplexVector([0] * 3 + [1, 0]),
                ComplexVector([0] * 4 + [1]),
            ],
        )


class NormalizedEigenvectorsCheck(unittest.TestCase):
    def test_not_square(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvectors(
                ComplexMatrix([[1, 1], [3, 3], [4, 4]]),
            )

    def test_not_diagonal_or_two_by_two(self):
        with self.assertRaises(ValueError):
            complex_matrix_eigenvectors(
                ComplexMatrix([[1, 1, 0], [0, 1, 0], [0, 0, -1]]),
            )

    def test_2_by_2(self):
        self.assertEqual(
            normalized_complex_matrix_eigenvectors(ComplexMatrix([[4, 3], [-2, -3]])),
            [
                ComplexVector([3 / math.sqrt(10), -1 / math.sqrt(10)]),
                ComplexVector([1 / math.sqrt(5), -2 / math.sqrt(5)]),
            ],
        )

    def test_another_2_by_2_for_ordering(self):
        self.assertEqual(
            normalized_complex_matrix_eigenvectors(ComplexMatrix([[-1, 2], [1, 0]])),
            [
                ComplexVector([1 / math.sqrt(2), 1 / math.sqrt(2)]),
                ComplexVector([2 / math.sqrt(5), -1 / math.sqrt(5)]),
            ],
        )

    def test_large_diagonal(self):
        self.assertEqual(
            normalized_complex_matrix_eigenvectors(m5x5),
            [
                ComplexVector([1] + [0] * 4),
                ComplexVector([0, 1] + [0] * 3),
                ComplexVector([0] * 2 + [1] + [0] * 2),
                ComplexVector([0] * 3 + [1, 0]),
                ComplexVector([0] * 4 + [1]),
            ],
        )


class ComplexVectorAdjointCheck(unittest.TestCase):
    def test_adjoint_small_case(self):
        self.assertEqual(
            complex_vector_adjoint(
                ComplexVector([1, 2, ComplexNumber(4, 5), ComplexNumber(-1, -1)])
            ),
            [[1], [2], [ComplexNumber(4, -5)], [ComplexNumber(-1, 1)]],
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
