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
        self.assertEqual(ComplexNumber.add(ComplexNumber(1, 1), ComplexNumber(3, 2)), ComplexNumber(4, 3))
    
    def test_add_negative_re(self):
        self.assertEqual(ComplexNumber.add(ComplexNumber(1, 1), ComplexNumber(-2, 0)), ComplexNumber(-1, 1))

class ComplexNumberMultiplyCheck(unittest.TestCase):

    def test_multiply_i_i(self):
        self.assertEqual(ComplexNumber.multiply(ComplexNumber(0, 1), ComplexNumber(0, 1)), ComplexNumber(-1, 0))

if __name__ == "__main__":
    unittest.main()
