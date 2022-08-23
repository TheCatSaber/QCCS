import unittest

from context import caesar_decode, caesar_encode


class CaesarShiftCheck(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(caesar_encode("MOO1&abcAzZxy", 3), "PRR1&defDcCab")

    def test_decode(self):
        self.assertEqual(caesar_decode("MOO1&abcdAzZxyW", 4), "IKK1&wxyzWvVtuS")


if __name__ == "__main__":
    unittest.main()
