import unittest

from context import (
    ComplexMatrix,
    ComplexVector,
    ComplexNumber,
    complex_matrix_vector_multiply,
)

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
minus_one = ComplexNumber(-1, 0)

v2 = ComplexVector([ComplexNumber(2, 1), ComplexNumber(1, 1)])
i2 = ComplexMatrix([[one, zero], [zero, one]])
rotation_90_2D = ComplexMatrix([[zero, minus_one], [one, zero]])


class ComplexMatrixVectorMultiplicationCheck(unittest.TestCase):
    def test_2_by_2_identity(self):
        self.assertEqual(complex_matrix_vector_multiply(i2, v2), v2)

    def test_2_by_2_rotation(self):
        self.assertEqual(
            complex_matrix_vector_multiply(rotation_90_2D, v2),
            ComplexVector([ComplexNumber(-1, -1), ComplexNumber(2, 1)]),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
