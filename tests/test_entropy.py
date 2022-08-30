import unittest

from context import (
    Shannon_entropy,
    SymbolProbability,
    verify_classical_pdf,
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


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
