import math
import unittest

from context import (
    BinaryTree,
    ComplexVector,
    Huffman_coding,
    Huffman_create_coding,
    QubitProbability,
    Shannon_entropy,
    SymbolProbability,
    density_operator,
    typical_sequences,
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
    def test_verifying_PDF(self):
        with self.assertRaises(ValueError):
            Shannon_entropy([])
        with self.assertRaises(ValueError):
            Shannon_entropy([SymbolProbability("A", 0.5)])
        with self.assertRaises(ValueError):
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.1),
                    SymbolProbability("D", 0.1),
                ]
            )
        with self.assertRaises(ValueError):
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("A", 0.5),
                ]
            )

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
    def test_verifying_PDF(self):
        with self.assertRaises(ValueError):
            density_operator([])
        with self.assertRaises(ValueError):
            density_operator([QubitProbability("A", ComplexVector([1, 0]), 0.5)])
        with self.assertRaises(ValueError):
            density_operator(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("B", ComplexVector([1, 0]), 0.25),
                    QubitProbability("C", ComplexVector([1, 0]), 0.1),
                    QubitProbability("D", ComplexVector([1, 0]), 0.1),
                ]
            )
        with self.assertRaises(ValueError):
            density_operator(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                ]
            )
        with self.assertRaises(ValueError):
            density_operator([QubitProbability("A", ComplexVector([1]), 1)])

        with self.assertRaises(ValueError):
            density_operator([QubitProbability("A", ComplexVector([1, 0, 0]), 1)])
        with self.assertRaises(ValueError):
            verify_quantum_pdf([QubitProbability("A", ComplexVector([1, 1]), 1)])

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
    def test_verifying_PDF(self):
        with self.assertRaises(ValueError):
            von_Neumann_entropy([])
        with self.assertRaises(ValueError):
            von_Neumann_entropy([QubitProbability("A", ComplexVector([1, 0]), 0.5)])
        with self.assertRaises(ValueError):
            von_Neumann_entropy(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("B", ComplexVector([1, 0]), 0.25),
                    QubitProbability("C", ComplexVector([1, 0]), 0.1),
                    QubitProbability("D", ComplexVector([1, 0]), 0.1),
                ]
            )
        with self.assertRaises(ValueError):
            von_Neumann_entropy(
                [
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                    QubitProbability("A", ComplexVector([1, 0]), 0.5),
                ]
            )
        with self.assertRaises(ValueError):
            von_Neumann_entropy([QubitProbability("A", ComplexVector([1]), 1)])

        with self.assertRaises(ValueError):
            von_Neumann_entropy([QubitProbability("A", ComplexVector([1, 0, 0]), 1)])
        with self.assertRaises(ValueError):
            von_Neumann_entropy([QubitProbability("A", ComplexVector([1, 1]), 1)])

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


class TypicalSequencesCheck(unittest.TestCase):
    def test_verifying_PDF(self):
        with self.assertRaises(ValueError):
            typical_sequences([], 2)
        with self.assertRaises(ValueError):
            typical_sequences([SymbolProbability("A", 0.5)], 2)
        with self.assertRaises(ValueError):
            typical_sequences(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.1),
                    SymbolProbability("D", 0.1),
                ],
                2,
            )
        with self.assertRaises(ValueError):
            typical_sequences(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("A", 0.5),
                ],
                2,
            )

    def test_bit_verification(self):
        with self.assertRaises(ValueError):
            typical_sequences(
                [
                    SymbolProbability("0", 0.5),
                    SymbolProbability("1", 0.25),
                    SymbolProbability("2", 0.25),
                ],
                1,
            )
        with self.assertRaises(ValueError):
            typical_sequences(
                [SymbolProbability("0", 0.5), SymbolProbability("2", 0.5)], 1
            )

    def test_value_verification(self):
        with self.assertRaises(ValueError):
            typical_sequences(
                [SymbolProbability("0", 0.5), SymbolProbability("1", 0.5)], 0
            )
        typical_sequences([SymbolProbability("0", 0.5), SymbolProbability("1", 0.5)], 1)

    def test_small_examples(self):
        self.assertEqual(
            typical_sequences(
                [SymbolProbability("0", 0.5), SymbolProbability("1", 0.5)], 2
            ),
            [[0, 1], [1, 0]],
        )
        self.assertEqual(
            typical_sequences(
                [SymbolProbability("0", 0.5), SymbolProbability("1", 0.5)], 3
            ),
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        )
        self.assertEqual(
            typical_sequences(
                [SymbolProbability("0", 1 / 3), SymbolProbability("1", 2 / 3)], 3
            ),
            [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        )

    def test_one_larger_example(self):
        self.assertEqual(
            typical_sequences(
                [SymbolProbability("0", 1 / 8), SymbolProbability("1", 7 / 8)], 8
            ),
            [[1] * i + [0] + [1] * (7 - i) for i in range(8)],
        )


class BinaryTreeCheck(unittest.TestCase):
    def test___eq__(self):
        self.assertEqual(
            BinaryTree(1, "a", None, None), BinaryTree(1.0, "a", None, None)
        )
        self.assertEqual(
            BinaryTree(1, "a", None, None), BinaryTree(1 + 1e-8, "a", None, None)
        )


class HuffmanCodingCheck(unittest.TestCase):
    wikipedia_case = [
        SymbolProbability("a", 0.10),
        SymbolProbability("b", 0.15),
        SymbolProbability("c", 0.30),
        SymbolProbability("d", 0.16),
        SymbolProbability("e", 0.29),
    ]
    wikipedia_tree = BinaryTree(
        1,
        None,
        left=BinaryTree(
            0.41,
            None,
            left=BinaryTree(0.16, "d", None, None),
            right=BinaryTree(
                0.25,
                None,
                left=BinaryTree(0.10, "a", None, None),
                right=BinaryTree(0.15, "b", None, None),
            ),
        ),
        right=BinaryTree(
            0.59,
            None,
            left=BinaryTree(0.29, "e", None, None),
            right=BinaryTree(0.30, "c", None, None),
        ),
    )
    two_items_case = [
        SymbolProbability("a", 0.28),
        SymbolProbability("b", 0.72),
    ]
    two_items_tree = BinaryTree(
        1,
        None,
        left=BinaryTree(0.28, "a", None, None),
        right=BinaryTree(0.72, "b", None, None),
    )

    def test_verifying_PDF(self):
        with self.assertRaises(ValueError):
            Shannon_entropy([])
        with self.assertRaises(ValueError):
            Shannon_entropy([SymbolProbability("A", 0.5)])
        with self.assertRaises(ValueError):
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("B", 0.25),
                    SymbolProbability("C", 0.1),
                    SymbolProbability("D", 0.1),
                ]
            )
        with self.assertRaises(ValueError):
            Shannon_entropy(
                [
                    SymbolProbability("A", 0.5),
                    SymbolProbability("A", 0.5),
                ]
            )

    def test_one_item(self):
        self.assertEqual(
            Huffman_coding([SymbolProbability("a", 1)]), BinaryTree(1, "a", None, None)
        )

    def test_two_items(self):
        self.assertEqual(Huffman_coding(self.two_items_case), self.two_items_tree)

    def test_small_wikipedia_case(self):
        self.assertEqual(Huffman_coding(self.wikipedia_case), self.wikipedia_tree)

    def test_conversion_to_binary_code_single_item(self):
        # Empty list, as no information to convey
        self.assertDictEqual(
            Huffman_create_coding(BinaryTree(1, "a", None, None)), {"a": []}
        )

    def test_conversion_to_binary_code_two_items(self):
        self.assertDictEqual(
            Huffman_create_coding(self.two_items_tree), {"a": [0], "b": [1]}
        )

    def test_conversion_to_binary_codes_wikipedia_case(self):
        self.assertDictEqual(
            Huffman_create_coding(self.wikipedia_tree),
            {"a": [0, 1, 0], "b": [0, 1, 1], "c": [1, 1], "d": [0, 0], "e": [1, 0]},
        )


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
