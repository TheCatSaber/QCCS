import math
import unittest

from context import (
    ComplexNumber,
    ComplexVector,
    state_probability,
    transition_amplitude,
)

minus_one = ComplexNumber(-1, 0)
zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)

sqrt_2_by_2 = ComplexNumber(1 / math.sqrt(2), 0)


negative_i = ComplexNumber(0, -1)
i = ComplexNumber(0, 1)

one_i = ComplexVector([one, i])
one_minus_i = ComplexVector([one, negative_i])
i_minus_one = ComplexVector([i, minus_one])
i_one = ComplexVector([i, one])


class StateProbabilityCheck(unittest.TestCase):
    def test_normalized(self):
        self.assertEqual(1, state_probability(ComplexVector([one, zero]), 0))

    def test_non_normalized(self):
        self.assertEqual(0.5, state_probability(ComplexVector([one, negative_i]), 0))


class TransitionAmplitudeCheck(unittest.TestCase):
    def test_normalized(self):
        self.assertEqual(
            negative_i,
            transition_amplitude(
                one_i.scalar_multiplication(sqrt_2_by_2),
                i_minus_one.scalar_multiplication(sqrt_2_by_2),
            ),
        )

    def test_non_normalized(self):
        self.assertEqual(negative_i, transition_amplitude(one_minus_i, i_one))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
