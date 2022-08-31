import math
import unittest

from context import (
    ComplexVector,
    QubitProbability,
    Shannon_entropy,
    SymbolProbability,
    density_operator,
    verify_classical_pdf,
    verify_quantum_pdf,
    von_Neumann_entropy,
)


class VerifyClassicalPDFCheck(unittest.TestCase):
    def test_verify_nothing(self):
        with self.assertRaises(ValueError):
            verify_classical_pdf([])

    def test_verify_single_thing_not_one(self):
        with self.assertRaises(ValueError):
            verify_classical_pdf([SymbolProbability("A", 0.5)])

    def test_verify_multiple_items(self):
        with self.assertRaises(ValueError):
            verify_classical_pdf(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.1),
                    SymbolProbability("D", 0.1),
                ]
            )

    def test_verify_two_items_of_same_type(self):
        with self.assertRaises(ValueError):
            verify_classical_pdf(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("A", 0.5),
                ]
            )


class ShannonEntropyCheck(unittest.TestCase):
    def test_uniform_pdf(self):
        self.assertEqual(
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.25),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.25),
                    SymbolProbability("D", 0.25),
                ]
            ),
            2,
        )

    def test_non_uniform_pdf(self):
        self.assertEqual(
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.125),
                    SymbolProbability("D", 0.125),
                ]
            ),
            1.75,
        )


class VerifyQuantumPDFCheck(unittest.TestCase):
    def test_verify_nothing(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf([])

    def test_verify_single_thing_not_one(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf([QubitProbability("A", ComplexVector([1, 0]), 0.5)])

    def test_verify_multiple_items(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("B", ComplexVector([1, 0]), 0.25),
                    QubitProbability("C", ComplexVector([1, 0]), 0.1),
                    QubitProbability("D", ComplexVector([1, 0]), 0.1),
                ]
            )

    def test_verify_two_items_of_same_type(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                ]
            )

    def test_verify_non_qubit_len_one(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf([QubitProbability("A", ComplexVector([1]), 1)])

    def test_verify_non_qubit_len_three(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf([QubitProbability("A", ComplexVector([1, 0, 0]), 1)])

    def test_non_normalized_qubit(self):
        with self.assertRaises(ValueError):
            verify_quantum_pdf([QubitProbability("A", ComplexVector([1, 1]), 1)])


class DensityOperatorCheck(unittest.TestCase):
    def test_plus_minus_operator(self):
        self.assertEqual(
            density_operator(
                [
                    QubitProbability(
                        "A", ComplexVector([1 / math.sqrt(2), 1 / math.sqrt(2)]), 1 / 4
                    ),
                    QubitProbability(
                        "B", ComplexVector([1 / math.sqrt(2), -1 / math.sqrt(2)]), 3 / 4
                    ),
                ]
            ),
            [[1 / 2, -1 / 4], [-1 / 4, 1 / 2]],
        )

    def test_plus_zero_operator(self):
        self.assertEqual(
            density_operator(
                [
                    QubitProbability(
                        "A", ComplexVector([1 / math.sqrt(2), 1 / math.sqrt(2)]), 1 / 3
                    ),
                    QubitProbability("B", ComplexVector([1, 0]), 2 / 3),
                ]
            ),
            [[5 / 6, 1 / 6], [1 / 6, 1 / 6]],
        )


class VonNeumannEntropyCheck(unittest.TestCase):
    def test_plus_zero_entropy(self):
        self.assertAlmostEqual(
            von_Neumann_entropy(
                [
                    QubitProbability(
                        "A",
                        ComplexVector([1 / math.sqrt(2), 1 / math.sqrt(2)]),
                        1 / 3,
                    ),
                    QubitProbability("B", ComplexVector([1, 0]), 2 / 3),
                ]
            ),
            0.550047759,
        )

    def test_plus_minus_entropy(self):
        self.assertAlmostEqual(
            von_Neumann_entropy(
                [
                    QubitProbability(
                        "A",
                        ComplexVector([1 / math.sqrt(2), 1 / math.sqrt(2)]),
                        1 / 4,
                    ),
                    QubitProbability(
                        "B",
                        ComplexVector([1 / math.sqrt(2), -1 / math.sqrt(2)]),
                        3 / 4,
                    ),
                ]
            ),
            0.8112781245,
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
