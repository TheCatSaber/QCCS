import unittest

from context import ComplexNumber, ComplexMatrix, ComplexVector, MarbleGame

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)
two = ComplexNumber(2, 0)
three = ComplexNumber(3, 0)
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


class MarbleGameInitFailuresCheck(unittest.TestCase):
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
            ComplexVector([ComplexNumber(-1, 0)]),
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
            v1,
            m1,
        )

    def test_movement_matrix_not_0_1(self):
        self.assertRaises(
            ValueError,
            MarbleGame,
            1,
            1,
            v1,
            ComplexMatrix([[ComplexNumber(-1, 0)]]),
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


class MarbleGameCheckEvolution(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
