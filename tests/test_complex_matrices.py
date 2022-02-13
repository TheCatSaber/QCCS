import unittest

from context import ComplexMatrix, complex_matrix_add

m2x3 = ComplexMatrix([[1, 2], [3, 4], [5, 6]])
m3x2 = ComplexMatrix([[1, 2, 3], [4, 5, 6]])
m3x3 = ComplexMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


class ComplexMatrixInitCheck(unittest.TestCase):
    def test_normal_init(self):
        ComplexMatrix([[1, 2], [3, 4]])

    def test_init_fails_with_different_lengths(self):
        with self.assertRaises(ValueError):
            ComplexMatrix([[1, 2], [3]])

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
        self.assertEqual(m3x3.get_row(0), [1, 2, 3])

    def test_row_max(self):
        self.assertEqual(m3x3.get_row(2), [7, 8, 9])

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
            ComplexMatrix([[1, 2, 3], [4, 5, 6]]), ComplexMatrix([[1, 2, 3], [4, 5, 6]])
        )

    def test_wrong_type(self):
        self.assertNotEqual(ComplexMatrix([[1]]), 1)

    def test_wrong_width(self):
        self.assertNotEqual(ComplexMatrix([[1, 2], [3, 4]]), ComplexMatrix([[1], [2]]))

    def test_wrong_height(self):
        self.assertNotEqual(ComplexMatrix([[1, 2]]), ComplexMatrix([[1, 2], [3, 4]]))

    def test_wrong_elements(self):
        self.assertNotEqual(ComplexMatrix([[1]]), ComplexMatrix([[2]]))


class ComplexMatrixAddCheck(unittest.TestCase):
    def test_different_widths(self):
        self.assertRaises(
            ValueError,
            complex_matrix_add,
            ComplexMatrix([[1, 2]]),
            ComplexMatrix([[1, 2, 3]]),
        )

    def test_different_heights(self):
        self.assertRaises(
            ValueError,
            complex_matrix_add,
            ComplexMatrix([[1, 2], [1, 2]]),
            ComplexMatrix(([[2, 1]])),
        )

    def test_width_one_height_one(self):
        self.assertEqual(
            complex_matrix_add(ComplexMatrix([[1]]), ComplexMatrix([[2]])),
            ComplexMatrix([[3]]),
        )


class ComplexMatrixInverseCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(ComplexMatrix([[1]]).inverse(), ComplexMatrix([[-1]]))

    def test_larger_inverse(self):
        self.assertEqual(
            m3x2.inverse(),
            ComplexMatrix([[-1, -2, -3], [-4, -5, -6]]),
        )


class ComplexMatrixScalarCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(
            ComplexMatrix([[1]]).scalar_multiplication(-2), ComplexMatrix([[-2]])
        )

    def test_larger_scalar_multiplication(self):
        self.assertEqual(
            m3x2.scalar_multiplication(4),
            ComplexMatrix([[4, 8, 12], [16, 20, 24]]),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
