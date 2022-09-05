import unittest

from context import (
    ComplexMatrix,
    ComplexNumber,
    ComplexVector,
    complex_matrix_eigenvalues,
    complex_matrix_eigenvectors,
    complex_matrix_vector_multiply,
    complex_vector_adjoint,
)

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
minus_one = ComplexNumber(-1, 0)
minus_two = ComplexNumber(-2, 0)
minus_three = ComplexNumber(-3, 0)
two = ComplexNumber(2, 0)
three = ComplexNumber(3, 0)
four = ComplexNumber(4, 0)

v2 = ComplexVector([ComplexNumber(2, 1), ComplexNumber(1, 1)])
i2 = ComplexMatrix([[one, zero], [zero, one]])
rotation_90_2D = ComplexMatrix([[zero, minus_one], [one, zero]])

m5x5 = ComplexMatrix(
    [
        [one] + [zero] * 4,
        [zero, three] + [zero] * 3,
        [zero] * 2 + [four] + [zero] * 2,
        [zero] * 3 + [minus_one, zero],
        [zero] * 4 + [minus_two],
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
        self.assertRaises(
            ValueError,
            complex_matrix_eigenvalues,
            ComplexMatrix([[one, one], [three, three], [four, four]]),
        )

    def test_not_diagonal_or_two_by_two(self):
        self.assertRaises(
            ValueError,
            complex_matrix_eigenvalues,
            ComplexMatrix(
                [[one, one, zero], [zero, one, zero], [zero, zero, minus_one]]
            ),
        )

    def test_2_by_2(self):
        self.assertEqual(
            [three, minus_two],
            complex_matrix_eigenvalues(
                ComplexMatrix([[four, three], [minus_two, minus_three]])
            ),
        )

    def test_large_diagonal(self):
        self.assertEqual(
            [one, three, four, minus_one, minus_two],
            complex_matrix_eigenvalues(m5x5),
        )


class ComplexMatrixEigenvectorsCheck(unittest.TestCase):
    def test_not_square(self):
        self.assertRaises(
            ValueError,
            complex_matrix_eigenvectors,
            ComplexMatrix([[one, one], [three, three], [four, four]]),
        )

    def test_not_diagonal_or_two_by_two(self):
        self.assertRaises(
            ValueError,
            complex_matrix_eigenvectors,
            ComplexMatrix(
                [[one, one, zero], [zero, one, zero], [zero, zero, minus_one]]
            ),
        )

    def test_2_by_2(self):
        self.assertEqual(
            [
                ComplexVector([three, minus_one]),
                ComplexVector([one, minus_two]),
            ],
            complex_matrix_eigenvectors(
                ComplexMatrix([[four, three], [minus_two, minus_three]])
            ),
        )

    def test_another_2_by_2_for_ordering(self):
        self.assertEqual(
            [ComplexVector([one, one]), ComplexVector([two, minus_one])],
            complex_matrix_eigenvectors(ComplexMatrix([[minus_one, two], [one, zero]])),
        )

    def test_large_diagonal(self):
        self.assertEqual(
            [
                ComplexVector([one] + [zero] * 4),
                ComplexVector([zero, one] + [zero] * 3),
                ComplexVector([zero] * 2 + [one] + [zero] * 2),
                ComplexVector([zero] * 3 + [one, zero]),
                ComplexVector([zero] * 4 + [one]),
            ],
            complex_matrix_eigenvectors(m5x5),
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
