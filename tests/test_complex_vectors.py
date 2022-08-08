import math
import unittest

from context import (
    ComplexNumber,
    ComplexVector,
    complex_vector_distance,
    complex_vector_inner_product,
    complex_vector_tensor_product,
)

zero_vector = ComplexVector([0])
v1 = ComplexVector([ComplexNumber(1, 1)])
v2 = ComplexVector([ComplexNumber(2, 1), ComplexNumber(1, 1)])
v5 = ComplexVector(
    [
        0,
        ComplexNumber(3, 1),
        ComplexNumber(2, -1),
        ComplexNumber(-1, 2),
        ComplexNumber(-5, -10),
    ],
)

v5_1 = [ComplexNumber(1, 1), ComplexNumber(2, 1), ComplexNumber(3, 2), 2, 1.1]
v5_2 = [
    ComplexNumber(2, 1),
    2,
    1.1,
    ComplexNumber(3.4, 3),
    ComplexNumber(3, 4),
]
v5_3 = [
    ComplexNumber(3, 2),
    ComplexNumber(4, 1),
    ComplexNumber(4.1, 2),
    ComplexNumber(5.4, 3),
    ComplexNumber(4.1, 4),
]


class ComplexVectorGetItemCheck(unittest.TestCase):
    def test_access_elements(self):
        self.assertEqual(ComplexNumber(1, 1), v2[1])

    def test_access_elements_from_real(self):
        self.assertEqual(ComplexVector([1.1, 2])[0], ComplexNumber(1.1, 0))

    def test_invalid_index_high(self):
        with self.assertRaises(IndexError):
            v2[2]

    def test_negative_index(self):
        self.assertEqual(v2[-1], ComplexNumber(1, 1))


class ComplexVectorSizeCheck(unittest.TestCase):
    def test_size_two(self):
        self.assertEqual(len(v2), 2)


class ComplexVectorEqualityCheck(unittest.TestCase):
    def test_equal_wrong_type(self):
        self.assertFalse(v1 == "a")

    def test_equal_different_lengths(self):
        self.assertFalse(v1 == v2)

    def test_equal_single_different_item(self):
        self.assertFalse(v1 == ComplexVector([ComplexNumber(1, 2)]))

    def test_equal_single_same_item(self):
        # Create new ComplexVector, to prove not checking same object.
        self.assertTrue(v1 == ComplexVector([ComplexNumber(1, 1)]))

    def test_equal_same_object(self):
        self.assertTrue(v2 == v2)

    def test_equality_with_list(self):
        self.assertTrue(v2 == [ComplexNumber(2, 1), ComplexNumber(1, 1)])

    def test_equality_with_list_with_real_numbers(self):
        self.assertTrue(
            ComplexVector([ComplexNumber(2.1, 0), ComplexNumber(1, 0)]) == [2.1, 1]
        )

    def test_non_equality_with_list(self):
        self.assertFalse(v2 == [ComplexNumber(3, 1), ComplexNumber(1, 1)])

    def test_non_equality_with_list_with_reals(self):
        self.assertFalse(ComplexVector([2.1, 2]) == [2.1, 1])


class ComplexVectorAdditionCheck(unittest.TestCase):
    def test___add___two_complex_vectors(self):
        self.assertEqual(ComplexVector(v5_1) + ComplexVector(v5_2), v5_3)

    def test___add___list(self):
        self.assertEqual(ComplexVector(v5_1) + v5_2, v5_3)
        self.assertEqual(v5_1 + ComplexVector(v5_2), v5_3)

    def test___add___different_lengths_error(self):
        with self.assertRaises(ValueError):
            _ = v1 + v2

    def test___add___wrong_type(self):
        with self.assertRaises(TypeError):
            _ = v1 + 1
        with self.assertRaises(TypeError):
            _ = 1 + v1
        with self.assertRaises(TypeError):
            _ = v1 + ["1"]
        with self.assertRaises(TypeError):
            _ = ["1"] + v1


class ComplexVectorSubtractCheck(unittest.TestCase):
    def test___sub___two_complex_vectors(self):
        self.assertEqual(ComplexVector(v5_3) - ComplexVector(v5_2), v5_1)

    def test___sub___list(self):
        self.assertEqual(ComplexVector(v5_3) - v5_2, v5_1)

    def test___rsub___list(self):
        self.assertEqual(v5_3 - ComplexVector(v5_2), v5_1)

    def test___sub_wrong_type(self):
        with self.assertRaises(TypeError):
            _ = v1 - 1
        with self.assertRaises(TypeError):
            _ = 1 - v1
        with self.assertRaises(TypeError):
            _ = v1 - ["1"]
        with self.assertRaises(TypeError):
            _ = ["1"] - v1

    def test___add___different_lengths_error(self):
        with self.assertRaises(ValueError):
            _ = v1 - v2


class ComplexVectorInverseCheck(unittest.TestCase):
    def test_zero_vector(self):
        self.assertEqual(zero_vector.inverse(), zero_vector)

    def test_v1(self):
        self.assertEqual(v1.inverse(), [ComplexNumber(-1, -1)])

    def test_5_element(self):
        self.assertEqual(
            v5.inverse(),
            [
                0,
                ComplexNumber(-3, -1),
                ComplexNumber(-2, 1),
                ComplexNumber(1, -2),
                ComplexNumber(5, 10),
            ],
        )


class ComplexVectorScalarMultiplicationCheck(unittest.TestCase):
    def test___rmul___zero(self):
        self.assertEqual(0 * v1, [0])

    def test___rmul___int(self):
        self.assertEqual(
            3 * ComplexVector([1, ComplexNumber(3, 2), ComplexNumber(1, 2)]),
            [3, ComplexNumber(9, 6), ComplexNumber(3, 6)],
        )

    def test___rmul___float(self):
        self.assertEqual(
            -2.4 * ComplexVector([1, ComplexNumber(3, 2), ComplexNumber(1, 2)]),
            ComplexVector([-2.4, ComplexNumber(-7.2, -4.8), ComplexNumber(-2.4, -4.8)]),
        )

    def test___rmul___complex_number(self):
        # Worked out using a calculator that supports complex numbers
        # Should probably have used a smaller example, or one from the textbook
        self.assertEqual(
            ComplexNumber(3, 2) * v5,
            ComplexVector(
                [
                    0,
                    ComplexNumber(7, 9),
                    ComplexNumber(8, 1),
                    ComplexNumber(-7, 4),
                    ComplexNumber(5, -40),
                ],
            ),
        )

    def test___rmul___wrong_type(self):
        with self.assertRaises(TypeError):
            _ = [""] * v1
        with self.assertRaises(TypeError):
            _ = v1 * v1


class ComplexVectorInnerProductCheck(unittest.TestCase):
    def test_inner_product_invalid_length(self):
        self.assertRaises(ValueError, complex_vector_inner_product, v1, v2)

    def test_inner_product_zero_vector(self):
        self.assertEqual(complex_vector_inner_product(zero_vector, zero_vector), 0)

    def test_inner_product_length_5_vectors(self):
        self.assertEqual(
            complex_vector_inner_product(
                v5,
                ComplexVector(
                    [
                        ComplexNumber(1, 3),
                        ComplexNumber(1, -1),
                        ComplexNumber(2, 4),
                        ComplexNumber(2.5, 3),
                        1,
                    ]
                ),
            ),
            ComplexNumber(0.5, 8),
        )


class ComplexVectorNormCheck(unittest.TestCase):
    def test_zero_vector(self):
        self.assertEqual(zero_vector.norm(), 0)

    def test_three_d_real_vector(self):
        self.assertEqual(
            ComplexVector([3, -6, 2]).norm(),
            7,
        )

    def test_complex_vector(self):
        self.assertEqual(
            ComplexVector(
                [
                    ComplexNumber(4, 3),
                    ComplexNumber(6, -4),
                    ComplexNumber(12, -7),
                    ComplexNumber(0, 13),
                ]
            ).norm(),
            math.sqrt(439),
        )


class ComplexVectorNormSquaredCheck(unittest.TestCase):
    def test_zero_vector(self):
        self.assertEqual(zero_vector.norm_squared(), 0)

    def test_three_d_real_vector(self):
        self.assertEqual(
            ComplexVector([3, -6, 2]).norm_squared(),
            49,
        )

    def test_complex_vector(self):
        self.assertEqual(
            ComplexVector(
                [
                    ComplexNumber(4, 3),
                    ComplexNumber(6, -4),
                    ComplexNumber(12, -7),
                    ComplexNumber(0, 13),
                ]
            ).norm_squared(),
            439,
        )


class ComplexVectorDistanceCheck(unittest.TestCase):
    def test_zero_vector_to_vector(self):
        self.assertEqual(
            complex_vector_distance(zero_vector, ComplexVector([ComplexNumber(5, 1)])),
            math.sqrt(26),
        )

    def test_distance_in_r_cubed(self):
        self.assertEqual(
            complex_vector_distance(
                ComplexVector([3, 1, 2]),
                ComplexVector([2, 2, -1]),
            ),
            math.sqrt(11),
        )


class ComplexVectorTensorProductCheck(unittest.TestCase):
    def test_two_three(self):
        self.assertEqual(
            complex_vector_tensor_product(
                ComplexVector([1, 0]),
                ComplexVector(
                    [ComplexNumber(0, 1), ComplexNumber(2, 3), ComplexNumber(3, 4)]
                ),
            ),
            ComplexVector(
                [
                    ComplexNumber(0, 1),
                    ComplexNumber(2, 3),
                    ComplexNumber(3, 4),
                    0,
                    0,
                    0,
                ]
            ),
        )

    def test_more_complex_tensor(self):
        self.assertEqual(
            complex_vector_tensor_product(
                ComplexVector([1, ComplexNumber(0, 1), 5]),
                ComplexVector(
                    [
                        2,
                        ComplexNumber(-1, -1),
                    ]
                ),
            ),
            [
                2,
                ComplexNumber(-1, -1),
                ComplexNumber(0, 2),
                ComplexNumber(1, -1),
                10,
                ComplexNumber(-5, -5),
            ],
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
