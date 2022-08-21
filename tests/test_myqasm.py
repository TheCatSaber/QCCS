import math
import unittest

from context import (
    MYQASM,
    ComplexMatrix,
    ComplexVector,
    InvalidMYQASMSyntaxError,
    KeywordEnum,
    MYQASM_lexer,
    TokenNameEnum,
    get_registers,
    get_user_defined_gates,
)


class LexerCheck(unittest.TestCase):
    def test_initialize_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("INITIALIZE R 5"),
            [
                (TokenNameEnum.KEYWORD, KeywordEnum.INITIALIZE),
                (TokenNameEnum.IDENTIFIER, "R"),
                (TokenNameEnum.LITERAL, "5"),
            ],
        )

    def test_initialize_lexing_defined_state(self):
        self.assertEqual(
            MYQASM_lexer("INITIALIZE R1_a 4 [0110]"),
            [
                (TokenNameEnum.KEYWORD, KeywordEnum.INITIALIZE),
                (TokenNameEnum.IDENTIFIER, "R1_a"),
                (TokenNameEnum.LITERAL, "4"),
                (TokenNameEnum.SEPARATOR, "["),
                (TokenNameEnum.LITERAL, "0110"),
                (TokenNameEnum.SEPARATOR, "]"),
            ],
        )

    def test_initialize_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R( 5")
        self.assertRaises(
            InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R 4 0110]"
        )
        self.assertRaises(
            InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R 4 [0110"
        )
        self.assertRaises(
            InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R 4 [0120]"
        )
        self.assertRaises(
            InvalidMYQASMSyntaxError, MYQASM_lexer, "INITIALIZE R 4 [01101]"
        )

    def test_select_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("SELECT S-1 R 2 4"),
            [
                (TokenNameEnum.KEYWORD, KeywordEnum.SELECT),
                (TokenNameEnum.IDENTIFIER, "S-1"),
                (TokenNameEnum.IDENTIFIER, "R"),
                (TokenNameEnum.LITERAL, "2"),
                (TokenNameEnum.LITERAL, "4"),
            ],
        )

    def test_select_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "SELECT R S 1")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "SELECT () S 1 2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "SELECT R * 1 2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "SELECT R S one 2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "SELECT R S 12 2_")

    def test_apply_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("APPLY U R"),
            [
                (TokenNameEnum.KEYWORD, KeywordEnum.APPLY),
                (TokenNameEnum.IDENTIFIER, "U"),
                (TokenNameEnum.IDENTIFIER, "R"),
            ],
        )

    def test_apply_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "APPLY U")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "APPLY () R")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "APPLY U ()")

    def test_measure_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("MEASURE R"),
            [
                (TokenNameEnum.KEYWORD, KeywordEnum.MEASURE),
                (TokenNameEnum.IDENTIFIER, "R"),
            ],
        )

    def test_measure_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "MEASURE R1 P")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "MEASURE (")

    def test_initial_identifier_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "(")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "( 1")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "controlled_H")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U BOB")

    def test_concat_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("U CONCAT R0.5 U2"),
            [
                (TokenNameEnum.IDENTIFIER, "U"),
                (TokenNameEnum.KEYWORD, KeywordEnum.CONCAT),
                (TokenNameEnum.IDENTIFIER, "R0.5"),
                (TokenNameEnum.IDENTIFIER, "U2"),
            ],
        )

    def test_concat_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U CONCAT U1")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U CONCAT * U2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U CONCAT U1 ()")

    def test_tensor_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("U TENSOR U1 U2"),
            [
                (TokenNameEnum.IDENTIFIER, "U"),
                (TokenNameEnum.KEYWORD, KeywordEnum.TENSOR),
                (TokenNameEnum.IDENTIFIER, "U1"),
                (TokenNameEnum.IDENTIFIER, "U2"),
            ],
        )

    def test_tensor_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U TENSOR U1")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U TENSOR * U2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U TENSOR U1 ()")

    def test_inverse_lexing_normal(self):
        self.assertEqual(
            MYQASM_lexer("U INVERSE U1"),
            [
                (TokenNameEnum.IDENTIFIER, "U"),
                (TokenNameEnum.KEYWORD, KeywordEnum.INVERSE),
                (TokenNameEnum.IDENTIFIER, "U1"),
            ],
        )

    def test_inverse_lexing_invalid(self):
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U INVERSE U1 U2")
        self.assertRaises(InvalidMYQASMSyntaxError, MYQASM_lexer, "U INVERSE *")


class MYQASMCheck(unittest.TestCase):
    def test_initialize_normal(self):
        MYQASM("INITIALIZE R 5")
        self.assertEqual(get_registers()["R"], ComplexVector([1] + [0] * 31))

    def test_initialize_with_given_qubits(self):
        MYQASM("INITIALIZE RA 4 [0110]")
        self.assertEqual(get_registers()["RA"], ComplexVector([0] * 6 + [1] + [0] * 9))

    def test_initialize_no_gate_name_register(self):
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE H 4")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE CNOT 4")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE I1 4")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE I2 4")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE R1 4")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE R0.5 4")

    def test_concat(self):
        MYQASM("A CONCAT H H")
        self.assertEqual(get_user_defined_gates()["A"], ComplexMatrix.identity(2))
        MYQASM("B CONCAT A H")
        self.assertEqual(
            get_user_defined_gates()["B"],
            ComplexMatrix(
                [
                    [1 / math.sqrt(2), 1 / math.sqrt(2)],
                    [1 / math.sqrt(2), -1 / math.sqrt(2)],
                ]
            ),
        )
        MYQASM("C CONCAT I4 CNOT")
        self.assertEqual(
            get_user_defined_gates()["C"],
            ComplexMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
        )
        MYQASM("D CONCAT R1 I2")
        self.assertEqual(
            get_user_defined_gates()["D"], ComplexMatrix([[1, 0], [0, -1]])
        )

    def test_concat_invalid(self):
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE REGISTER 1")
            MYQASM("REGISTER CONCAT H H")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("F CONCAT U H")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("F CONCAT H U")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("F CONCAT H CNOT")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("I2 CONCAT H H")

    def test_measure(self):
        MYQASM("INITIALIZE REG1 5")
        ans = MYQASM("MEASURE REG1")
        self.assertEqual(ans, [0, 0, 0, 0, 0])
        MYQASM("INITIALIZE REG2 4 [0110]")
        ans = MYQASM("MEASURE REG2")
        self.assertEqual(ans, [0, 1, 1, 0])

    def test_measure_invalid(self):
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("MEASURE REG_INFINITY")

    def test_tensor(self):
        MYQASM("T1 TENSOR I2 H")
        self.assertEqual(
            get_user_defined_gates()["T1"],
            ComplexMatrix(
                [
                    [1 / math.sqrt(2), 1 / math.sqrt(2), 0, 0],
                    [1 / math.sqrt(2), -1 / math.sqrt(2), 0, 0],
                    [0, 0, 1 / math.sqrt(2), 1 / math.sqrt(2)],
                    [0, 0, 1 / math.sqrt(2), -1 / math.sqrt(2)],
                ]
            ),
        )
        MYQASM("T2 TENSOR H H")
        self.assertEqual(
            get_user_defined_gates()["T2"],
            ComplexMatrix(
                [
                    [
                        1 / 2,
                        1 / 2,
                        1 / 2,
                        1 / 2,
                    ],
                    [
                        1 / 2,
                        -1 / 2,
                        1 / 2,
                        -1 / 2,
                    ],
                    [
                        1 / 2,
                        1 / 2,
                        -1 / 2,
                        -1 / 2,
                    ],
                    [
                        1 / 2,
                        -1 / 2,
                        -1 / 2,
                        1 / 2,
                    ],
                ]
            ),
        )

    def test_tensor_invalid(self):
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("INITIALIZE REGISTER 1")
            MYQASM("REGISTER TENSOR H H")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("F TENSOR U H")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("F TENSOR H U")
        with self.assertRaises(InvalidMYQASMSyntaxError):
            MYQASM("I2 TENSOR H H")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
