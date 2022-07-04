import math
import unittest

from context import (
    ComplexNumber,
    complex_number_add,
    complex_number_divide,
    complex_number_multiply,
    complex_number_subtract,
)


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
            complex_number_add(ComplexNumber(1, 1), ComplexNumber(3, 2)),
            ComplexNumber(4, 3),
        )

    def test_add_negative_re(self):
        self.assertEqual(
            complex_number_add(ComplexNumber(1, 1), ComplexNumber(-2, 0)),
            ComplexNumber(-1, 1),
        )


class ComplexNumberSubtractCheck(unittest.TestCase):
    def test_subtract_positive(self):
        self.assertEqual(
            complex_number_subtract(ComplexNumber(3, 3), ComplexNumber(3, 2)),
            ComplexNumber(0, 1),
        )


class ComplexNumberMultiplyCheck(unittest.TestCase):
    def test_multiply_i_i(self):
        self.assertEqual(
            complex_number_multiply(ComplexNumber(0, 1), ComplexNumber(0, 1)),
            ComplexNumber(-1, 0),
        )


class ComplexNumberDivideCheck(unittest.TestCase):
    def test_divide_book_example(self):
        self.assertEqual(
            complex_number_divide(ComplexNumber(-2, 1), ComplexNumber(1, 2)),
            ComplexNumber(0, 1),
        )

    def test_throw_value_error(self):
        self.assertRaises(
            ValueError, complex_number_divide, ComplexNumber(-2, 1), ComplexNumber(0, 0)
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
        self.assertEqual(ComplexNumber(1, 1).conjugate(), ComplexNumber(1, -1))

    def test_conjugate_neg_pos(self):
        self.assertEqual(ComplexNumber(1, -2).conjugate(), ComplexNumber(1, 2))

    def test_conjugate_zero(self):
        self.assertEqual(ComplexNumber(2, 0).conjugate(), ComplexNumber(2, 0))


class ComplexNumberPolarFormCheck(unittest.TestCase):
    one_one = ComplexNumber(1, 1)
    sqrt_2_pi_by_4 = (math.sqrt(2), math.pi / 4)

    def test_to_polar(self):
        self.assertEqual(self.one_one.to_polar(), self.sqrt_2_pi_by_4)

    def _from_polar_setup(self):
        return ComplexNumber.new_from_polar(*self.sqrt_2_pi_by_4)

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


class ComplexNumberIsTypeOfNumberCheck(unittest.TestCase):
    minus_point_two = ComplexNumber(-0.2, 0)

    def test_is_real_true(self):
        self.assertTrue(self.minus_point_two.is_real())

    def test_is_real_false(self):
        self.assertFalse(ComplexNumber(-0.2, 1).is_real())

    def test_is_positive_real_true(self):
        self.assertTrue(ComplexNumber(0.2, 0).is_positive_real())

    def test_is_positive_real_false_negative(self):
        self.assertFalse(self.minus_point_two.is_positive_real())

    def test_is_positive_real_false_not_real(self):
        self.assertFalse(ComplexNumber(0.2, 1).is_positive_real())

    def test_is_integer_true(self):
        self.assertTrue(ComplexNumber(-2, 0).is_integer())

    def test_is_integer_false_but_real(self):
        self.assertFalse(self.minus_point_two.is_integer())

    def test_is_integer_false_not_real(self):
        self.assertFalse(ComplexNumber(-2, -1).is_integer())

    def test_is_positive_integer_true(self):
        self.assertTrue(ComplexNumber(2, 0).is_positive_integer())

    def test_is_positive_integer_false_but_positive(self):
        self.assertFalse(ComplexNumber(2.2, 0).is_positive_integer())

    def test_is_positive_integer_false_negative(self):
        self.assertFalse(ComplexNumber(-2, 0).is_positive_integer())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
