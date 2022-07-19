import math
import unittest

from context import (
    ComplexMatrix,
    ComplexNumber,
    ComplexVector,
    observable_mean,
    observable_variance,
    state_probability,
    transition_amplitude,
)

minus_one = ComplexNumber(-1, 0)
zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
two = ComplexNumber(2, 0)
four = ComplexNumber(4, 0)

sqrt_2_by_2 = ComplexNumber(1 / math.sqrt(2), 0)


negative_i = ComplexNumber(0, -1)
i = ComplexNumber(0, 1)

one_i = ComplexVector([one, i])
one_minus_i = ComplexVector([one, negative_i])
i_minus_one = ComplexVector([i, minus_one])
i_one = ComplexVector([i, one])

m1 = ComplexMatrix([[one, negative_i], [i, two]])
m2 = ComplexMatrix([[two, zero], [zero, four]])


class StateProbabilityCheck(unittest.TestCase):
    def test_out_of_range_low(self):
        self.assertRaises(ValueError, state_probability, one_minus_i, -1)

    def test_out_of_range_high(self):
        self.assertRaises(ValueError, state_probability, one_minus_i, 2)

    def test_normalized(self):
        self.assertEqual(1, state_probability(ComplexVector([one, zero]), 0))

    def test_non_normalized(self):
        self.assertEqual(0.5, state_probability(one_minus_i, 0))


class TransitionAmplitudeCheck(unittest.TestCase):
    def test_differing_sizes(self):
        self.assertRaises(ValueError, transition_amplitude, one_i, ComplexVector([one]))

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


class ObservableMeanCheck(unittest.TestCase):
    def test_non_hermitian(self):
        self.assertRaises(
            ValueError, observable_mean, ComplexMatrix([[one, one], [one, i]]), one_i
        )

    def test_invalid_size(self):
        self.assertRaises(ValueError, observable_mean, m1, ComplexVector([one]))

    def test_two_variable_observable(self):
        self.assertEqual(
            ComplexNumber(2.5, 0),
            observable_mean(
                m1,
                one_i.scalar_multiplication(sqrt_2_by_2),
            ),
        )

    def test_two_variable_diagonal(self):
        self.assertEqual(
            ComplexNumber(3, 0),
            observable_mean(
                m2,
                one_i.scalar_multiplication(sqrt_2_by_2),
            ),
        )


class ObservableVarianceCheck(unittest.TestCase):
    def test_non_hermitian(self):
        self.assertRaises(
            ValueError, observable_mean, ComplexMatrix([[one, one], [one, i]]), one_i
        )

    def test_invalid_size(self):
        self.assertRaises(ValueError, observable_mean, m1, ComplexVector([one]))

    def test_non_diagonal_observable(self):
        self.assertEqual(
            ComplexNumber(0.25, 0),
            observable_variance(m1, one_i.scalar_multiplication(sqrt_2_by_2)),
        )

    def test_diagonal_observable(self):
        self.assertEqual(
            one, observable_variance(m2, one_i.scalar_multiplication(sqrt_2_by_2))
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
