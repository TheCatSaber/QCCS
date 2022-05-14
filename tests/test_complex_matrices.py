import unittest

from context import (
    ComplexMatrix,
    ComplexNumber,
    complex_matrix_add,
    complex_matrix_multiply,
)

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
two = ComplexNumber(2, 0)
three = ComplexNumber(3, 0)
four = ComplexNumber(4, 0)
five = ComplexNumber(5, 0)
six = ComplexNumber(6, 0)
seven = ComplexNumber(7, 0)
eight = ComplexNumber(8, 0)
nine = ComplexNumber(9, 0)

m2x2 = ComplexMatrix([[one, two], [three, four]])
m2x3 = ComplexMatrix([[one, two], [three, four], [five, six]])
m3x2 = ComplexMatrix([[one, two, three], [four, five, six]])
m3x3 = ComplexMatrix([[one, two, three], [four, five, six], [seven, eight, nine]])
i2 = ComplexMatrix([[one, zero], [zero, one]])


class ComplexMatrixInitCheck(unittest.TestCase):
    def test_normal_init(self):
        ComplexMatrix([[one, two], [three, four]])

    def test_init_fails_with_different_lengths(self):
        with self.assertRaises(ValueError):
            ComplexMatrix([[one, two], [three]])

    def test_zero_length_fails_init(self):
        with self.assertRaises(TypeError):
            ComplexMatrix([])

    def test_zero_width_fails_init(self):
        with self.assertRaises(ValueError):
            ComplexMatrix([[], []])


class ComplexMatrixGetWidthCheck(unittest.TestCase):
    def test_two_width(self):
        self.assertEqual(m2x3.get_width(), 2)

    def test_three_width(self):
        self.assertEqual(m3x2.get_width(), 3)


class ComplexMatrixGetHeightCheck(unittest.TestCase):
    def test_two_height(self):
        self.assertEqual(m3x2.get_height(), 2)

    def test_three_height(self):
        self.assertEqual(m2x3.get_height(), 3)


class ComplexMatrixGetRowCheck(unittest.TestCase):
    def test_row_zero(self):
        self.assertEqual(m3x3.get_row(0), [one, two, three])

    def test_row_max(self):
        self.assertEqual(m3x3.get_row(2), [seven, eight, nine])

    def test_row_out_of_range(self):
        with self.assertRaises(ValueError):
            m3x3.get_row(3)

    def test_row_negative(self):
        # TODO: in the future, this should act like a negative index on a normal list.
        with self.assertRaises(ValueError):
            m3x3.get_row(-1)


class ComplexMatrixEqualCheck(unittest.TestCase):
    def test_are_equal(self):
        self.assertEqual(
            ComplexMatrix([[one, two, three], [four, five, six]]),
            ComplexMatrix([[one, two, three], [four, five, six]]),
        )

    def test_wrong_type(self):
        self.assertNotEqual(ComplexMatrix([[one]]), 1)

    def test_wrong_width(self):
        self.assertNotEqual(
            ComplexMatrix([[one, two], [three, four]]), ComplexMatrix([[one], [two]])
        )

    def test_wrong_height(self):
        self.assertNotEqual(ComplexMatrix([[one, two, three]]), m3x2)

    def test_wrong_elements(self):
        self.assertNotEqual(ComplexMatrix([[one]]), ComplexMatrix([[two]]))


class ComplexMatrixAddCheck(unittest.TestCase):
    def test_different_widths(self):
        self.assertRaises(
            ValueError,
            complex_matrix_add,
            ComplexMatrix([[one, two]]),
            ComplexMatrix([[one, two, three]]),
        )

    def test_different_heights(self):
        self.assertRaises(
            ValueError,
            complex_matrix_add,
            ComplexMatrix([[one, two], [one, two]]),
            ComplexMatrix(([[two, one]])),
        )

    def test_width_one_height_one(self):
        self.assertEqual(
            complex_matrix_add(ComplexMatrix([[one]]), ComplexMatrix([[two]])),
            ComplexMatrix([[three]]),
        )


class ComplexMatrixInverseCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(
            ComplexMatrix([[one]]).inverse(), ComplexMatrix([[ComplexNumber(-1, 0)]])
        )

    def test_larger_inverse(self):
        self.assertEqual(
            m3x2.inverse(),
            ComplexMatrix(
                [
                    [ComplexNumber(-1, 0), ComplexNumber(-2, 0), ComplexNumber(-3, 0)],
                    [ComplexNumber(-4, 0), ComplexNumber(-5, 0), ComplexNumber(-6, 0)],
                ]
            ),
        )

    def test_complex_number(self):
        self.assertEqual(
            ComplexMatrix([[ComplexNumber(1, 1)]]).inverse(),
            ComplexMatrix([[ComplexNumber(-1, -1)]]),
        )


class ComplexMatrixScalarCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(
            ComplexMatrix([[two]]).scalar_multiplication(ComplexNumber(-3, 0)),
            ComplexMatrix([[ComplexNumber(-6, 0)]]),
        )

    def test_larger_scalar_multiplication(self):
        self.assertEqual(
            m3x2.scalar_multiplication(ComplexNumber(0, 2)),
            ComplexMatrix(
                [
                    [ComplexNumber(0, 2), ComplexNumber(0, 4), ComplexNumber(0, 6)],
                    [ComplexNumber(0, 8), ComplexNumber(0, 10), ComplexNumber(0, 12)],
                ]
            ),
        )


class ComplexMatrixConjugateCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(
            ComplexMatrix([[ComplexNumber(0, -1)]]).conjugate(),
            ComplexMatrix([[ComplexNumber(0, 1)]]),
        )

    def test_larger_matrix_conjugate(self):
        self.assertEqual(
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, -1)],
                    [ComplexNumber(0, 1), ComplexNumber(2, 1)],
                ]
            ).conjugate(),
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, 1)],
                    [ComplexNumber(0, -1), ComplexNumber(2, -1)],
                ]
            ),
        )


class ComplexMatrixTransposeCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(ComplexMatrix([[two]]).transpose(), ComplexMatrix([[two]]))

    def test_larger_matrix_transpose(self):
        self.assertEqual(
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, -1), ComplexNumber(0, 3)],
                    [ComplexNumber(0, 1), ComplexNumber(2, 1), ComplexNumber(3, -1)],
                ]
            ).transpose(),
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, 1)],
                    [ComplexNumber(0, -1), ComplexNumber(2, 1)],
                    [ComplexNumber(0, 3), ComplexNumber(3, -1)],
                ]
            ),
        )


class ComplexMatrixAdjointCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(ComplexMatrix([[two]]).adjoint(), ComplexMatrix([[two]]))

    def test_larger_matrix_adjoint(self):
        self.assertEqual(
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, -1), ComplexNumber(0, 3)],
                    [ComplexNumber(0, 1), ComplexNumber(2, 1), ComplexNumber(3, -1)],
                ]
            ).adjoint(),
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, -1)],
                    [ComplexNumber(0, 1), ComplexNumber(2, -1)],
                    [ComplexNumber(0, -3), ComplexNumber(3, 1)],
                ]
            ),
        )


class ComplexMatrixMultiplicationCheck(unittest.TestCase):
    def test_wrong_size_rejected(self):
        self.assertRaises(
            ValueError,
            complex_matrix_multiply,
            ComplexMatrix([[one, two], [three, four]]),
            m2x3,
        )

    def test_two_by_two_by_identity(self):
        self.assertEqual(complex_matrix_multiply(m2x2, i2), m2x2)

    def test_different_sizes(self):
        self.assertEqual(
            complex_matrix_multiply(
                ComplexMatrix(
                    [
                        [six, ComplexNumber(0, -1), ComplexNumber(5, 2)],
                        [seven, nine, ComplexNumber(-2, -1)],
                    ]
                ),
                ComplexMatrix([[one, ComplexNumber(0, 1)], [two, three], [four, five]]),
            ),
            ComplexMatrix(
                [
                    [ComplexNumber(26, 6), ComplexNumber(25, 13)],
                    [ComplexNumber(17, -4), ComplexNumber(17, 2)],
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
