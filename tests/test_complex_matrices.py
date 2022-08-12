import math
import unittest

from context import ComplexMatrix, ComplexNumber, tensor_product

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
two = ComplexNumber(2, 0)
three = ComplexNumber(3, 0)
four = ComplexNumber(4, 0)
five = ComplexNumber(5, 0)
six = ComplexNumber(6, 0)

one_over_root_two = ComplexNumber(1 / math.sqrt(2), 0)
half = ComplexNumber(1 / 2, 0)

m2x2 = ComplexMatrix([[1, 2], [3, 4]])
m2x3 = ComplexMatrix([[1, 2], [3, 4], [5, 6]])
m3x2 = ComplexMatrix([[1, 2, 3], [4, 5, 6]])
m3x3 = ComplexMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
i2 = ComplexMatrix([[1, 0], [0, 1]])


class ComplexMatrixInitCheck(unittest.TestCase):
    def test_normal_init(self):
        ComplexMatrix([[1, 2], [3, 4]])
        ComplexMatrix([[1, 2.1]])

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


class ComplexMatrixGetColumnCheck(unittest.TestCase):
    def test_column_zero(self):
        self.assertEqual(m3x3.get_column(0), [1, 4, 7])

    def test_row_max(self):
        self.assertEqual(m3x3.get_column(2), [3, 6, 9])

    def test_column_out_of_range(self):
        with self.assertRaises(ValueError):
            m3x3.get_column(3)

    def test_column_negative(self):
        # TODO: in the future, this should act like a negative index on a normal list.
        with self.assertRaises(ValueError):
            m3x3.get_column(-1)


class ComplexMatrixEqualCheck(unittest.TestCase):
    def test___eq___are_equal(self):
        self.assertEqual(
            ComplexMatrix([[one, two, three], [four, five, six]]),
            ComplexMatrix([[1, 2, 3], [4, 5, 6]]),
        )

    def test___eq___wrong_type(self):
        self.assertNotEqual(ComplexMatrix([[one]]), 1)

    def test___eq___wrong_width(self):
        self.assertNotEqual(
            ComplexMatrix([[one, two], [three, four]]), ComplexMatrix([[one], [two]])
        )
        self.assertNotEqual([[one, two], [three, four]], ComplexMatrix([[one], [two]]))
        self.assertNotEqual(ComplexMatrix([[one, two], [three, four]]), [[one], [two]])

    def test___eq___wrong_height(self):
        self.assertNotEqual(ComplexMatrix([[one, two, three]]), m3x2)
        self.assertNotEqual(([[one, two, three]]), m3x2)
        self.assertNotEqual(m3x2, ([[one, two, three]]))

    def test___eq___wrong_elements(self):
        self.assertNotEqual(ComplexMatrix([[one]]), ComplexMatrix([[two]]))

    def test___eq___with_list(self):
        self.assertEqual(
            ComplexMatrix([[one, two, three], [four, five, six]]),
            [[1, 2, 3], [4, 5, 6]],
        )

    def test___eq___list_with_float(self):
        self.assertEqual(
            ComplexMatrix([[1.2, 3], [-4, ComplexNumber(4, 5.6)]]),
            [[1.2, 3], [-4, ComplexNumber(4, 5.6)]],
        )


class ComplexMatrixAddCheck(unittest.TestCase):
    def test___add___different_widths(self):
        with self.assertRaises(ValueError):
            _ = ComplexMatrix([[1, 2]]) + ComplexMatrix([[1, 2, 3]])

    def test___add___different_heights(self):
        with self.assertRaises(ValueError):
            _ = ComplexMatrix([[1, 2], [1, 2]]) + ComplexMatrix(([[2, 1]]))
        with self.assertRaises(ValueError):
            _ = ComplexMatrix([[1, 2], [1, 2]]) + ([[2, 1]])
        with self.assertRaises(ValueError):
            _ = [[1, 2], [1, 2]] + ComplexMatrix(([[2, 1]]))

    def test___add___width_one_height_one(self):
        self.assertEqual(ComplexMatrix([[1]]) + ComplexMatrix([[2]]), [[3]])

    def test___add___not_ComplexMatrix(self):
        self.assertEqual(
            ComplexMatrix([[1, 2, 3], [1.1, 2.2, 3.3]]) + [[1, 2, 4], [-1, -2, -3]],
            [[2, 4, 7], [0.1, 0.2, 0.3]],
        )
        self.assertEqual(
            [[1, 2, 4], [-1, -2, -3]] + ComplexMatrix([[1, 2, 3], [1.1, 2.2, 3.3]]),
            [[2, 4, 7], [0.1, 0.2, 0.3]],
        )

    def test___add___wrong_type(self):
        with self.assertRaises(TypeError):
            _ = ComplexMatrix([[1]]) + []
        with self.assertRaises(TypeError):
            _ = [] + ComplexMatrix([[1]])
        with self.assertRaises(TypeError):
            _ = ComplexMatrix([[1]]) + "1"
        with self.assertRaises(TypeError):
            _ = "1" + ComplexMatrix([[1]])


class ComplexMatrixMultiplicationCheck(unittest.TestCase):
    def test___mul___wrong_size_rejected(self):
        with self.assertRaises(ValueError):
            _ = ComplexMatrix([[1, 2], [3, 4]]) * m2x3

    def test___mul___two_by_two_by_identity(self):
        self.assertEqual(m2x2 * i2, m2x2)

    def test___mul___different_sizes(self):
        self.assertEqual(
            ComplexMatrix(
                [
                    [6, ComplexNumber(0, -1), ComplexNumber(5, 2)],
                    [7, 9, ComplexNumber(-2, -1)],
                ]
            )
            * ComplexMatrix([[1, ComplexNumber(0, 1)], [2, 3], [4, 5]]),
            [
                [ComplexNumber(26, 6), ComplexNumber(25, 13)],
                [ComplexNumber(17, -4), ComplexNumber(17, 2)],
            ],
        )

    def test__mul___wrong_type(self):
        with self.assertRaises(TypeError):
            _ = ComplexMatrix([[1]]) * []
        with self.assertRaises(TypeError):
            _ = [] * ComplexMatrix([[1]])
        with self.assertRaises(TypeError):
            _ = ComplexMatrix([[1]]) * "1"
        with self.assertRaises(TypeError):
            _ = "1" * ComplexMatrix([[1]])
        with self.assertRaises(TypeError):
            _ = ComplexMatrix([[1]]) * 1

    def test___rmul___one_by_one(self):
        self.assertEqual(
            -3 * ComplexMatrix([[2]]),
            [[-6]],
        )

    def test___rmul___float_scalar(self):
        self.assertEqual(
            4.5 * ComplexMatrix([[2, 5]]),
            [[9, 22.5]],
        )

    def test___rmul___larger_scalar_multiplication(self):
        self.assertEqual(
            ComplexNumber(0, 2) * m3x2,
            [
                [ComplexNumber(0, 2), ComplexNumber(0, 4), ComplexNumber(0, 6)],
                [ComplexNumber(0, 8), ComplexNumber(0, 10), ComplexNumber(0, 12)],
            ],
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
        self.assertEqual(ComplexMatrix([[2]]).transpose(), ComplexMatrix([[2]]))

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
                    [1, ComplexNumber(0, 1)],
                    [ComplexNumber(0, -1), ComplexNumber(2, 1)],
                    [ComplexNumber(0, 3), ComplexNumber(3, -1)],
                ]
            ),
        )


class ComplexMatrixAdjointCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertEqual(ComplexMatrix([[2]]).adjoint(), ComplexMatrix([[2]]))

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
                    [1, ComplexNumber(0, -1)],
                    [ComplexNumber(0, 1), ComplexNumber(2, -1)],
                    [ComplexNumber(0, -3), ComplexNumber(3, 1)],
                ]
            ),
        )


class ComplexMatrixIsHermitianCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertTrue(ComplexMatrix([[two]]).is_hermitian())

    def test_larger_not_hermitian(self):
        self.assertFalse(
            ComplexMatrix(
                [
                    [one, ComplexNumber(0, -1), ComplexNumber(0, 3)],
                    [ComplexNumber(0, 1), ComplexNumber(2, 1), ComplexNumber(3, -1)],
                ]
            ).is_hermitian(),
        )

    def test_larger_is_hermitian(self):
        self.assertTrue(
            ComplexMatrix(
                [
                    [5, ComplexNumber(4, 5), ComplexNumber(6, -16)],
                    [ComplexNumber(4, -5), ComplexNumber(13, 0), 7],
                    [ComplexNumber(6, 16), 7, ComplexNumber(-2.1, 0)],
                ]
            ).is_hermitian()
        )


class ComplexMatrixIsUnitaryCheck(unittest.TestCase):
    def test_one_by_one(self):
        self.assertTrue(ComplexMatrix([[one]]).is_unitary())

    def test_three_by_three(self):
        root_2_over_2 = 1 / math.sqrt(2)
        complex_root_2_over_2 = ComplexNumber(root_2_over_2, 0)
        self.assertTrue(
            ComplexMatrix(
                [
                    [complex_root_2_over_2, ComplexNumber(-root_2_over_2, 0), 0],
                    [complex_root_2_over_2, complex_root_2_over_2, 0],
                    [0, 0, 1],
                ]
            ).is_unitary()
        )

    def test_two_by_two_false(self):
        self.assertFalse(ComplexMatrix([[2, 1], [1, 2]]).is_unitary())


class ComplexMatrixIdentityCheck(unittest.TestCase):
    def test_invalid_n(self):
        self.assertRaises(ValueError, ComplexMatrix.identity, 0)

    def test_one_by_one(self):
        self.assertEqual(ComplexMatrix.identity(1), ComplexMatrix([[1]]))

    def test_larger(self):
        self.assertEqual(
            ComplexMatrix.identity(3),
            ComplexMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        )


class ComplexMatrixTensorProductCheck(unittest.TestCase):
    def test_two_vectors(self):
        self.assertEqual(
            tensor_product(ComplexMatrix([[2], [3]]), ComplexMatrix([[4], [6], [3]])),
            [[8], [12], [6], [12], [18], [9]],
        )

    def test_matrices(self):
        self.assertEqual(
            tensor_product(
                ComplexMatrix([[1, 2], [3, 4]]),
                ComplexMatrix([[1, ComplexNumber(0, 1), 3], [5, 6, 1]]),
            ),
            ComplexMatrix(
                [
                    [1, ComplexNumber(0, 1), 3, 2, ComplexNumber(0, 2), 6],
                    [5, 6, 1, 10, 12, 2],
                    [
                        3,
                        ComplexNumber(0, 3),
                        9,
                        4,
                        ComplexNumber(0, 4),
                        12,
                    ],
                    [
                        15,
                        18,
                        3,
                        20,
                        24,
                        4,
                    ],
                ]
            ),
        )


class ComplexMatrixIsSquareCheck(unittest.TestCase):
    def test_two_by_two(self):
        self.assertTrue(m2x2.is_square())

    def test_two_by_three(self):
        self.assertFalse(m2x3.is_square())


class ComplexMatrixModuliSquaredMatrixCheck(unittest.TestCase):
    def test_small_case(self):
        self.assertEqual(
            ComplexMatrix(
                [[one_over_root_two, one_over_root_two], [1, 1]]
            ).moduli_squared_matrix(),
            ComplexMatrix([[0.5, 0.5], [1, 1]]),
        )

    def test_larger_case_including_complex_values(self):
        self.assertEqual(
            ComplexMatrix(
                [
                    [
                        1,
                        12,
                        0,
                        ComplexNumber(1 / math.sqrt(6), 1 / math.sqrt(6)),
                    ],
                    [
                        ComplexNumber(0, 1),
                        ComplexNumber(-1 / math.sqrt(2), 0),
                        ComplexNumber(0, -1 / math.sqrt(5)),
                        ComplexNumber(-1 / math.sqrt(6), 1 / math.sqrt(6)),
                    ],
                ]
            ).moduli_squared_matrix(),
            ComplexMatrix(
                [
                    [1, 144, 0, 1 / 3],
                    [1, 0.5, 1 / 5, 1 / 3],
                ]
            ),
        )


class ComplexMatrixIsDiagonalCheck(unittest.TestCase):
    def test_two_by_two_yes(self):
        self.assertTrue(ComplexMatrix([[1, 0], [0, 5]]).is_diagonal())

    def test_two_by_two_no(self):
        self.assertFalse(m2x2.is_diagonal())

    def test_two_by_three(self):
        self.assertFalse(m2x3.is_diagonal())

    def test_larger(self):
        self.assertTrue(
            ComplexMatrix(
                [
                    [1, 0, 0, 0, 0],
                    [0, 5, 0, 0, 0],
                    [0, 0, 3, 0, 0],
                    [0, 0, 0, ComplexNumber(0, 1), 0],
                    [0, 0, 0, 0, ComplexNumber(1, 1)],
                ]
            ).is_diagonal()
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
