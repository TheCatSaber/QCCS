import math
import unittest

from context import (
    ComplexNumber,
    ComplexVector,
    complex_vector_add,
    complex_vector_distance,
    complex_vector_inner_product,
)

zero_vector = ComplexVector([ComplexNumber(0, 0)])
v1 = ComplexVector([ComplexNumber(1, 1)])
v2 = ComplexVector([ComplexNumber(2, 1), ComplexNumber(1, 1)])
v5 = ComplexVector(
    [
        ComplexNumber(0, 0),
        ComplexNumber(3, 1),
        ComplexNumber(2, -1),
        ComplexNumber(-1, 2),
        ComplexNumber(-5, -10),
    ],
)


class ComplexVectorGetItemCheck(unittest.TestCase):
    def test_access_elements(self):
        self.assertEqual(ComplexNumber(1, 1), v2[1])

    def test_invalid_index_high(self):
        with self.assertRaises(IndexError):
            v2[2]

    def test_negative_index(self):
        self.assertEqual(ComplexNumber(1, 1), v2[-1])


class ComplexVectorSizeCheck(unittest.TestCase):
    def test_size_two(self):
        self.assertEqual(len(v2), 2)


class ComplexVectorEqualityCheck(unittest.TestCase):
    def test_equal_wrong_type(self):
        self.assertEqual(False, v1 == "a")

    def test_equal_different_lengths(self):
        self.assertEqual(False, v1 == v2)

    def test_equal_single_different_item(self):
        self.assertEqual(False, v1 == ComplexVector([ComplexNumber(1, 2)]))

    def test_equal_single_same_item(self):
        # Create new ComplexVector, to prove not checking same object.
        self.assertEqual(True, v1 == ComplexVector([ComplexNumber(1, 1)]))

    def test_equal_same_object(self):
        self.assertEqual(True, v2 == v2)


class ComplexVectorAdditionCheck(unittest.TestCase):
    def test_add_zero_vector(self):
        self.assertEqual(v1, complex_vector_add(v1, zero_vector))

    def test_add_v1_to_itself(self):
        self.assertEqual(
            ComplexVector([ComplexNumber(2, 2)]), complex_vector_add(v1, v1)
        )

    def test_different_lengths_error(self):
        self.assertRaises(ValueError, complex_vector_add, v1, v2)


class ComplexVectorInverseCheck(unittest.TestCase):
    def test_zero_vector(self):
        self.assertEqual(zero_vector, zero_vector.inverse())

    def test_v1(self):
        self.assertEqual(ComplexVector([ComplexNumber(-1, -1)]), v1.inverse())

    def test_5_element(self):

        self.assertEqual(
            ComplexVector(
                [
                    ComplexNumber(0, 0),
                    ComplexNumber(-3, -1),
                    ComplexNumber(-2, 1),
                    ComplexNumber(1, -2),
                    ComplexNumber(5, 10),
                ],
            ),
            v5.inverse(),
        )


class ComplexVectorScalarMultiplicationCheck(unittest.TestCase):
    def test_multiply_by_zero(self):
        self.assertEqual(zero_vector, v1.scalar_multiplication(ComplexNumber(0, 0)))

    def test_multiply_v5(self):
        # Worked out using a calculator that supports complex numbers
        # Should probably have used a smaller example, or one from the textbook
        self.assertEqual(
            ComplexVector(
                [
                    ComplexNumber(0, 0),
                    ComplexNumber(7, 9),
                    ComplexNumber(8, 1),
                    ComplexNumber(-7, 4),
                    ComplexNumber(5, -40),
                ],
            ),
            v5.scalar_multiplication(ComplexNumber(3, 2)),
        )


class ComplexVectorInnerProductCheck(unittest.TestCase):
    def test_inner_product_invalid_length(self):
        self.assertRaises(ValueError, complex_vector_inner_product, v1, v2)

    def test_inner_product_zero_vector(self):
        self.assertEqual(
            complex_vector_inner_product(zero_vector, zero_vector), ComplexNumber(0, 0)
        )

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
                        ComplexNumber(1, 0),
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
            ComplexVector(
                [ComplexNumber(3, 0), ComplexNumber(-6, 0), ComplexNumber(2, 0)]
            ).norm(),
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
            ComplexVector(
                [ComplexNumber(3, 0), ComplexNumber(-6, 0), ComplexNumber(2, 0)]
            ).norm_squared(),
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
        two = ComplexNumber(2, 0)
        self.assertEqual(
            complex_vector_distance(
                ComplexVector([ComplexNumber(3, 0), ComplexNumber(1, 0), two]),
                ComplexVector([two, two, ComplexNumber(-1, 0)]),
            ),
            math.sqrt(11),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
