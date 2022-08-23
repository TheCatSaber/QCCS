import unittest

from context import (
    caesar_decode,
    caesar_encode,
    one_time_pad_encode,
    one_time_pad_key_gen,
)


class CaesarShiftCheck(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(caesar_encode("MOO1&abcAzZxy", 3), "PRR1&defDcCab")

    def test_decode(self):
        self.assertEqual(caesar_decode("MOO1&abcdAzZxyW", 4), "IKK1&wxyzWvVtuS")


class OneTimePadCheck(unittest.TestCase):
    def test_key_gen_correct_chars_and_length(self):
        key = one_time_pad_key_gen(15)
        self.assertTrue(all(char in [0, 1] for char in key))
        self.assertEqual(len(key), 15)

    def test_OTP_encode(self):
        self.assertEqual(
            one_time_pad_encode(
                "a&÷ÿ",
                [
                    0,
                    1,
                    0,
                    1,
                    1,
                    0,
                    1,
                    1,
                    1,
                    1,
                    0,
                    1,
                    0,
                    0,
                    0,
                    1,
                    0,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                ],
            ),
            ":÷¹\x8c",
        )

    def test_OTP_decode(self):
        self.assertEqual(
            one_time_pad_encode(
                ":÷¹\x8c",
                [
                    0,
                    1,
                    0,
                    1,
                    1,
                    0,
                    1,
                    1,
                    1,
                    1,
                    0,
                    1,
                    0,
                    0,
                    0,
                    1,
                    0,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    1,
                ],
            ),
            "a&÷ÿ",
        )

    def test_OTP_invalid(self):
        with self.assertRaises(ValueError):
            one_time_pad_encode("a", [0, 0, 0])

        with self.assertRaises(ValueError):
            one_time_pad_encode(chr(256), [0] * 8)


if __name__ == "__main__":
    unittest.main()
