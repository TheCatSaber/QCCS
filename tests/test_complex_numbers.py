import math
import unittest

from context import ComplexNumber


class ComplexNumberInitCheck(unittest.TestCase):
    def test_real(self):
        self.assertEqual(1, ComplexNumber(1, 2).get_real())

    def test_im(self):
        self.assertEqual(2, ComplexNumber(1, 2).get_imaginary())

    def test___str___positive(self):
        self.assertEqual("1 + 2i", str(ComplexNumber(1, 2)))

    def test___str___negative(self):
        self.assertEqual("-1 - 3i", str(ComplexNumber(-1, -3)))

    def test___eq___same(self):
        self.assertTrue(ComplexNumber(1, 1) == ComplexNumber(1, 1))

    def test___eq___not_same_re(self):
        self.assertFalse(ComplexNumber(1, 1) == ComplexNumber(0, 1))

    def test___eq___not_same_im(self):
        self.assertFalse(ComplexNumber(1, 1) == ComplexNumber(1, 2))

    def test___eq___not_same_both(self):
        self.assertFalse(ComplexNumber(1, 1) == ComplexNumber(0, -1))

    def test___eq___wrong_type(self):
        self.assertFalse(ComplexNumber(1, 1) == 1)


class ComplexNumberAddCheck(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(
            ComplexNumber.add(ComplexNumber(1, 1), ComplexNumber(3, 2)),
            ComplexNumber(4, 3),
        )

    def test_add_negative_re(self):
        self.assertEqual(
            ComplexNumber.add(ComplexNumber(1, 1), ComplexNumber(-2, 0)),
            ComplexNumber(-1, 1),
        )


class ComplexNumberSubtractCheck(unittest.TestCase):
    def test_subtract_positive(self):
        self.assertEqual(
            ComplexNumber.subtract(ComplexNumber(3, 3), ComplexNumber(3, 2)),
            ComplexNumber(0, 1),
        )


class ComplexNumberMultiplyCheck(unittest.TestCase):
    def test_multiply_i_i(self):
        self.assertEqual(
            ComplexNumber.multiply(ComplexNumber(0, 1), ComplexNumber(0, 1)),
            ComplexNumber(-1, 0),
        )


class ComplexNumberDivideCheck(unittest.TestCase):
    def test_divide_book_example(self):
        self.assertEqual(
            ComplexNumber.divide(ComplexNumber(-2, 1), ComplexNumber(1, 2)),
            ComplexNumber(0, 1),
        )

    def test_throw_value_error(self):
        self.assertRaises(
            ValueError, ComplexNumber.divide, ComplexNumber(-2, 1), ComplexNumber(0, 0)
        )


class ComplexNumberModulusCheck(unittest.TestCase):
    def test_modulus_zero(self):
        self.assertEqual(ComplexNumber(0, 0).modulus(), 0)

    def test_modulus_3_4_5(self):
        self.assertEqual(ComplexNumber(3, 4).modulus(), 5)

    def test_modulus_4_3_5(self):
        self.assertEqual(ComplexNumber(4, 3).modulus(), 5)


class ComplexNumberConjugateCheck(unittest.TestCase):
    def test_conjugate_pos_neg(self):
        self.assertEqual(
            ComplexNumber.conjugate(ComplexNumber(1, 1)), ComplexNumber(1, -1)
        )

    def test_conjugate_neg_pos(self):
        self.assertEqual(
            ComplexNumber.conjugate(ComplexNumber(1, -2)), ComplexNumber(1, 2)
        )

    def test_conjugate_zero(self):
        self.assertEqual(
            ComplexNumber.conjugate(ComplexNumber(2, 0)), ComplexNumber(2, 0)
        )


class ComplexNumberPolarFormCheck(unittest.TestCase):
    one_one = ComplexNumber(1, 1)
    sqrt_2_pi_by_4 = (math.sqrt(2), math.pi / 4)

    def test_to_polar(self):
        self.assertEqual(self.one_one.to_polar(), self.sqrt_2_pi_by_4)

    def _from_polar_setup(self):
        return ComplexNumber.from_polar(*self.sqrt_2_pi_by_4)

    def test_from_polar_re(self):
        self.assertAlmostEqual(
            self._from_polar_setup().get_real(), self.one_one.get_real()
        )

    def test_from_polar_im(self):
        self.assertAlmostEqual(
            self._from_polar_setup().get_imaginary(), self.one_one.get_imaginary()
        )


class ComplexNumberInverseCheck(unittest.TestCase):
    def test_zero(self):
        zero_zero = ComplexNumber(0, 0)
        self.assertEqual(zero_zero, zero_zero.inverse())

    def test_one_one(self):
        self.assertEqual(ComplexNumber(-1, -1), ComplexNumber(1, 1).inverse())

    def test_two_minus_one(self):
        self.assertEqual(ComplexNumber(-2, 1), ComplexNumber(2, -1).inverse())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
