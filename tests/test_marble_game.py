import math
import unittest

from context import (
    ComplexMatrix,
    ComplexNumber,
    ComplexVector,
    InterferenceDetector,
    InterferenceDetectorOutput,
    MarbleGame,
    ProbabilisticMarbleGame,
    QuantumMarbleGame,
    complex_matrix_multiply,
    identity,
)

minus_one = ComplexNumber(-1, 0)
zero = ComplexNumber(0, 0)
sixth = ComplexNumber(1 / 6, 0)
third = ComplexNumber(1 / 3, 0)
half = ComplexNumber(0.5, 0)
one_over_root_two = ComplexNumber(1 / math.sqrt(2), 0)
one = ComplexNumber(1, 0)
two = ComplexNumber(2, 0)
three = ComplexNumber(3, 0)
i = ComplexNumber(0, 1)
v1 = ComplexVector([one])
v3 = ComplexVector([zero, two, three])
v6 = ComplexVector(
    [ComplexNumber(6, 0), two, one, ComplexNumber(5, 0), three, ComplexNumber(10, 0)]
)
m1 = ComplexMatrix([[one]])
m3 = ComplexMatrix([[one, zero, zero], [zero, zero, one], [zero, one, zero]])
six_zero_list = [zero] * 6
m6 = ComplexMatrix(
    [
        six_zero_list,
        six_zero_list,
        [zero, one, zero, zero, zero, one],
        [zero, zero, zero, one, zero, zero],
        [zero, zero, one, zero, zero, zero],
        [one, zero, zero, zero, one, zero],
    ]
)
game1 = MarbleGame(1, 1, v1, m1)
game3 = MarbleGame(3, 5, v3, m3)
game6 = MarbleGame(6, 27, v6, m6)

v_b = ComplexVector([one, zero, zero, zero, zero, zero, zero, zero])
m_b = ComplexMatrix(
    [
        [zero] * 8,
        [half] + [zero] * 7,
        [half] + [zero] * 7,
        [zero, third, zero, one] + [zero] * 4,
        [zero, third, zero, zero, one] + [zero] * 3,
        [zero, third, third, zero, zero, one] + [zero] * 2,
        [zero] * 2 + [third] + [zero] * 3 + [one, zero],
        [zero] * 2 + [third] + [zero] * 4 + [one],
    ]
)
game_b = ProbabilisticMarbleGame(8, 1, v_b, m_b)


class MarbleGameInitCheck(unittest.TestCase):
    def test_0_nodes(self):
        self.assertRaises(ValueError, MarbleGame, 0, 1, v1, m1)

    def test_0_marbles(self):
        self.assertRaises(ValueError, MarbleGame, 1, 0, v1, m1)

    def test_initial_state_negative(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            ComplexVector([minus_one]),
            m1,
        )

    def test_initial_state_not_integer(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            ComplexVector([ComplexNumber(0.5, 0)]),
            m1,
        )

    def test_initial_state_not_real(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            ComplexVector([ComplexNumber(1, 1)]),
            m1,
        )

    def test_initial_state_invalid_length(self):
        self.assertRaises(ValueError, MarbleGame, 2, 1, v1, m1)

    def test_initial_state_invalid_count(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            2,
            v1,
            m1,
        )

    def test_movement_matrix_not_square(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            v1,
            ComplexMatrix([[one], [one]]),
        )

    def test_movement_matrix_invalid_size(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            2,
            1,
            ComplexVector([one, zero]),
            m1,
        )

    def test_movement_matrix_not_0_1(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            v1,
            ComplexMatrix([[minus_one]]),
        )

    def test_movement_matrix_one_count(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            2,
            2,
            ComplexVector([one, one]),
            ComplexMatrix([[one, zero], [one, one]]),
        )


class MarbleGameIterationsCheck(unittest.TestCase):
    def test_iterations_must_be_positive(self):
        self.assertRaises(ValueError, game1.calculate_state, -1)

    def test_zero_iterations(self):
        self.assertEqual(v3, game3.calculate_state(0))

    def test_one_iteration(self):
        self.assertEqual(ComplexVector([zero, three, two]), game3.calculate_state(1))

    def test_two_iterations(self):
        self.assertEqual(v3, game3.calculate_state(2))

    def test_large_one_iteration(self):
        self.assertEqual(
            ComplexVector(
                [
                    zero,
                    zero,
                    ComplexNumber(12, 0),
                    ComplexNumber(5, 0),
                    one,
                    ComplexNumber(9, 0),
                ]
            ),
            game6.calculate_state(1),
        )


class ProbabilisticMarbleGameInitCheck(unittest.TestCase):
    def test_initial_state_sum(self):
        self.assertRaises(
            ValueError,
            ProbabilisticMarbleGame,
            3,
            1,
            ComplexVector([half, half, half]),
            m3,
        )

    def test_initial_state_negative_value(self):
        self.assertRaises(
            ValueError,
            ProbabilisticMarbleGame,
            3,
            1,
            ComplexVector([one, one, minus_one]),
            m3,
        )

    def test_invalid_matrix_column_sum(self):
        self.assertRaises(
            ValueError,
            ProbabilisticMarbleGame,
            3,
            1,
            ComplexVector([half, half, zero]),
            ComplexMatrix([[half, half, zero], [half, zero, half], [half, half, half]]),
        )

    def test_movement_matrix_negative_value(self):
        self.assertRaises(
            ValueError,
            ProbabilisticMarbleGame,
            3,
            5,
            v3,
            ComplexMatrix(
                [[minus_one, one, one], [one, zero, zero], [one, zero, zero]]
            ),
        )

    # There is no need to test with values greater than one for the movement matrix, and the sum
    # will be greater than 1, or there will be negative values present.


class ProbabilisticMarbleGameIterationsCheck(unittest.TestCase):
    def test_bullet_zero_iterations(self):
        self.assertEqual(v_b, game_b.calculate_state(0))

    def test_bullet_one_iteration(self):
        self.assertEqual(
            ComplexVector([zero, half, half] + [zero] * 5), game_b.calculate_state(1)
        )

    def test_bullet_two_iterations(self):
        self.assertEqual(
            ComplexVector([zero] * 3 + [sixth] * 2 + [third] + [sixth] * 2),
            game_b.calculate_state(2),
        )


class QuantumMarbleGameInitCheck(unittest.TestCase):
    def test_invalid_initial_state_sum(self):
        self.assertRaises(
            ValueError,
            QuantumMarbleGame,
            2,
            1,
            ComplexVector([half, half]),
            identity(2),
        )

    def test_invalid_column_sum(self):
        self.assertRaises(
            ValueError,
            QuantumMarbleGame,
            2,
            1,
            ComplexVector([one_over_root_two, one_over_root_two]),
            ComplexMatrix([[half, half], [half, half]]),
        )


class QuantumMarbleGameIterationCheck(unittest.TestCase):
    v = ComplexVector(
        [
            ComplexNumber(1 / math.sqrt(3), 0),
            ComplexNumber(0, 2 / math.sqrt(15)),
            ComplexNumber(math.sqrt(2 / 5), 0),
        ]
    )
    game = QuantumMarbleGame(
        3,
        1,
        v,
        ComplexMatrix(
            [
                [one_over_root_two, one_over_root_two, zero],
                [
                    ComplexNumber(0, -1 / math.sqrt(2)),
                    ComplexNumber(0, 1 / math.sqrt(2)),
                    zero,
                ],
                [zero, zero, i],
            ]
        ),
    )

    def test_zero_iterations(self):
        self.assertEqual(self.v, self.game.calculate_state(0))

    def test_one_iteration(self):
        self.assertEqual(
            ComplexVector(
                [
                    ComplexNumber(1 / math.sqrt(6), 2 / math.sqrt(30)),
                    ComplexNumber(-2 / math.sqrt(30), -1 / math.sqrt(6)),
                    ComplexNumber(0, math.sqrt(2 / 5)),
                ]
            ),
            self.game.calculate_state(1),
        )


class InterferenceDetectorInitCheck(unittest.TestCase):
    def test_zero_nodes(self):
        self.assertRaises(ValueError, InterferenceDetector, 0, ComplexMatrix([[one]]))

    def test_movement_matrix_errors_passed_through(self):
        self.assertRaises(
            ValueError, InterferenceDetector, 2, ComplexMatrix([[one, one], [one, one]])
        )


class InterferenceDetectorIterationsCheck(unittest.TestCase):
    p1 = ComplexNumber(-1 / math.sqrt(6), 1 / math.sqrt(6))
    p2 = ComplexNumber(-1 / math.sqrt(6), -1 / math.sqrt(6))
    p3 = ComplexNumber(1 / math.sqrt(6), -1 / math.sqrt(6))
    m = ComplexMatrix(
        [
            [zero] * 8,
            [one_over_root_two] + [zero] * 7,
            [one_over_root_two] + [zero] * 7,
            [zero, p1, zero, one] + [zero] * 4,
            [zero, p2] + [zero] * 2 + [one] + [zero] * 3,
            [zero, p3, p1] + [zero] * 2 + [one] + [zero] * 2,
            [zero] * 2 + [p2] + [zero] * 3 + [one, zero],
            [zero] * 2 + [p3] + [zero] * 4 + [one],
        ]
    )

    def test_one_iteration(self):
        self.assertRaises(
            ValueError,
            InterferenceDetector(1, ComplexMatrix([[one]])).calculate_interference,
            1,
        )

    def test_bullet_example(self):
        self.assertTupleEqual(
            # Just checking that the correct operations are performed for matrix multiplication
            # and modulus squaring, rather than checking the operations themselves are correct.
            # And that the interference is correctly detected.
            InterferenceDetectorOutput(
                self.m,
                complex_matrix_multiply(self.m, self.m),
                self.m.moduli_squared_matrix(),
                complex_matrix_multiply(self.m, self.m).moduli_squared_matrix(),
                [(5, 0)],
            ),
            InterferenceDetector(8, self.m).calculate_interference(2),
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
