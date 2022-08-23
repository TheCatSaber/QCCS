import unittest

from context import (
    AliceAnswer,
    BobAnswer,
    alice,
    bob,
    caesar_decode,
    caesar_encode,
    knuth,
    knuth2,
    one_time_pad_encode,
    one_time_pad_key_gen,
    random_bit_string,
)


class SharedCheck(unittest.TestCase):
    def test_random_bits(self):
        string = random_bit_string(17)
        self.assertTrue(all(char in [0, 1] for char in string))
        self.assertEqual(len(string), 17)


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


class BB84Check(unittest.TestCase):
    def test_alice_right_stuff(self):
        alice_answer = alice(10)
        self.assertEqual(len(alice_answer.bit_sent), 10)
        self.assertEqual(len(alice_answer.sending_basis), 10)
        self.assertTrue(all(bit in [0, 1] for bit in alice_answer.bit_sent))
        self.assertTrue(all(bit in [0, 1] for bit in alice_answer.sending_basis))

    def test_bob_right_stuff(self):
        bob_answer = bob(11)
        self.assertEqual(len(bob_answer.receiving_basis), 11)
        self.assertTrue(all(bit in [0, 1] for bit in bob_answer.receiving_basis))

    def test_knuth(self):
        alice_answer = AliceAnswer(
            [0, 1, 1, 0, 1],
            [
                1,
                0,
                1,
                0,
                1,
            ],
        )
        bob_answer = BobAnswer([0, 1, 1, 0, 0])
        knuth_answer = knuth(alice_answer, bob_answer)
        self.assertEqual(knuth_answer.bit_received[2], 1)
        self.assertEqual(knuth_answer.bit_received[3], 0)
        self.assertEqual(knuth_answer.proportion_measured_in_same_basis, 0.4)
        self.assertTrue(0.4 <= knuth_answer.proportion_correct <= 1)

    def test_knuth2(self):
        alice_answer = AliceAnswer(
            [0, 1, 1, 0, 1],
            [
                1,
                0,
                1,
                0,
                1,
            ],
        )
        bob_answer = BobAnswer([0, 1, 1, 0, 0])
        knuth2_answer = knuth2(alice_answer, bob_answer)
        self.assertEqual(knuth2_answer, [1, 0])


if __name__ == "__main__":
    unittest.main()
