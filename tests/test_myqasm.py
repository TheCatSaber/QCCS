import unittest

from context import InvalidMYQASMSyntaxError, KeywordEnum, MYQASM_lexer, TokenNameEnum


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


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
