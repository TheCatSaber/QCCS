import unittest

from context import ComplexNumber, ComplexVector

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
        self.assertEqual(v1, ComplexVector.add(v1, zero_vector))

    def test_add_v1_to_itself(self):
        self.assertEqual(
            ComplexVector([ComplexNumber(2, 2)]), ComplexVector.add(v1, v1)
        )

    def test_different_lengths_error(self):
        self.assertRaises(ValueError, ComplexVector.add, v1, v2)


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


if __name__ == "__main__":
    unittest.main()  # pragma: no cover