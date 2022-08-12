from enum import Enum, auto
from typing import Optional

from complex_vectors import ComplexVector

_registers: dict[str, ComplexVector] = {}


class TokenNameEnum(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    LITERAL = auto()
    SEPARATOR = auto()


class KeywordEnum(Enum):
    INITIALIZE = auto()
    SELECT = auto()
    CONCAT = auto()
    TENSOR = auto()
    INVERSE = auto()
    APPLY = auto()
    MEASURE = auto()


class InvalidMYQASMSyntaxError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_registers():
    return _registers


def MYQASM(expression: str) -> Optional[list[int]]:
    global _registers
    token_stream = MYQASM_lexer(expression)
    keyword = None
    for token in token_stream:
        if token[0] == TokenNameEnum.KEYWORD:
            keyword = token[1]
            assert isinstance(keyword, KeywordEnum)
            break
    assert keyword is not None
    match keyword:
        case KeywordEnum.INITIALIZE:
            identifier = token_stream[1][1]
            qubit_count = token_stream[2][1]
            assert isinstance(identifier, str)
            assert isinstance(qubit_count, str)
            v: list[int] = [1] + [0] * ((2 ** int(qubit_count)) - 1)
            if len(token_stream) == 6:
                initial_state = token_stream[4][1]
                assert isinstance(initial_state, str)
                v[0] = 0
                v[int(initial_state, 2)] = 1
            _registers[identifier] = ComplexVector(v)
            return None
        case _:
            pass


def _valid_identifier(identifier: str) -> None:
    if not all(char.isalnum() or char in "-_." for char in identifier):
        raise InvalidMYQASMSyntaxError("Invalid identifier name.")


def _valid_number(number: str, error_message: str = "Invalid number.") -> None:
    if not number.isdigit():
        raise InvalidMYQASMSyntaxError(error_message)


def MYQASM_lexer(
    expression: str,
) -> list[tuple[TokenNameEnum, str | KeywordEnum]]:
    token_list: list[tuple[TokenNameEnum, str | KeywordEnum]] = []
    string_list = expression.split(" ")
    number_of_strings = len(string_list)
    match (a := string_list[0]):
        case "INITIALIZE":
            token_list.append((TokenNameEnum.KEYWORD, KeywordEnum.INITIALIZE))
            if number_of_strings not in [3, 4]:
                raise InvalidMYQASMSyntaxError(
                    "INITIALIZE must be followed by followed by 2 or 3 strings."
                )

            identifier = string_list[1]
            _valid_identifier(identifier)
            token_list.append((TokenNameEnum.IDENTIFIER, identifier))

            qubit_count = string_list[2]
            _valid_number(
                qubit_count, f"`{a} {identifier}` must be followed by a number."
            )
            token_list.append((TokenNameEnum.LITERAL, qubit_count))

            if number_of_strings == 4:
                initial_state = string_list[3]
                if initial_state[0] != "[" or initial_state[-1] != "]":
                    raise InvalidMYQASMSyntaxError(
                        "Qubit register's initial state must be wrapped in square"
                        " brackets (`[` and `]`)."
                    )

                numbers = initial_state[1:-1]
                if any(char not in ["0", "1"] for char in numbers):
                    raise InvalidMYQASMSyntaxError(
                        "Each qubit's initial state must be either 0 or 1."
                    )

                if len(numbers) != int(qubit_count):
                    raise InvalidMYQASMSyntaxError(
                        "Qubit register's initial state's length must match number of"
                        " qubits."
                    )

                token_list.append((TokenNameEnum.SEPARATOR, "["))
                token_list.append((TokenNameEnum.LITERAL, numbers))
                token_list.append((TokenNameEnum.SEPARATOR, "]"))
        case "SELECT":
            token_list.append((TokenNameEnum.KEYWORD, KeywordEnum.SELECT))
            if number_of_strings != 5:
                raise InvalidMYQASMSyntaxError(
                    "INITIALIZE must be followed by followed by 4 strings."
                )
            identifier1 = string_list[1]
            identifier2 = string_list[2]
            _valid_identifier(identifier1)
            _valid_identifier(identifier2)

            token_list.append((TokenNameEnum.IDENTIFIER, identifier1))
            token_list.append((TokenNameEnum.IDENTIFIER, identifier2))

            number1 = string_list[3]
            number2 = string_list[4]
            error_message = (
                f"`{a} {identifier1} {identifier2}` must be followed by two numbers"
            )
            _valid_number(number1, error_message)
            _valid_number(number2, error_message)

            token_list.append((TokenNameEnum.LITERAL, number1))
            token_list.append((TokenNameEnum.LITERAL, number2))
        case "APPLY":
            token_list.append((TokenNameEnum.KEYWORD, KeywordEnum.APPLY))
            if number_of_strings != 3:
                raise InvalidMYQASMSyntaxError("APPLY must be followed by 2 strings.")

            identifier1 = string_list[1]
            identifier2 = string_list[2]
            _valid_identifier(identifier1)
            _valid_identifier(identifier2)

            token_list.append((TokenNameEnum.IDENTIFIER, identifier1))
            token_list.append((TokenNameEnum.IDENTIFIER, identifier2))
        case "MEASURE":
            token_list.append((TokenNameEnum.KEYWORD, KeywordEnum.MEASURE))
            if number_of_strings != 2:
                raise InvalidMYQASMSyntaxError("APPLY must be followed by 1 string.")

            identifier1 = string_list[1]
            _valid_identifier(identifier1)

            token_list.append((TokenNameEnum.IDENTIFIER, identifier1))
        case _:
            _valid_identifier(a)
            token_list.append((TokenNameEnum.IDENTIFIER, a))
            # length must be greater than 2, and second word must be CONCAT, TENSOR or INVERSE.
            if number_of_strings < 2:
                raise InvalidMYQASMSyntaxError("Cannot have an identifier by itself.")
            keyword = string_list[1]
            keyword_enum_value = None
            if keyword == "CONCAT":
                keyword_enum_value = KeywordEnum.CONCAT
            elif keyword == "TENSOR":
                keyword_enum_value = KeywordEnum.TENSOR
            elif keyword == "INVERSE":
                keyword_enum_value = KeywordEnum.INVERSE
            else:
                raise InvalidMYQASMSyntaxError(
                    "Invalid keyword following an identifier."
                )
            token_list.append((TokenNameEnum.KEYWORD, keyword_enum_value))
            if keyword in ["CONCAT", "TENSOR"]:
                if number_of_strings != 4:
                    raise InvalidMYQASMSyntaxError(
                        f"`{a} {keyword}` must be followed by 2 identifiers"
                    )
                identifier1 = string_list[2]
                identifier2 = string_list[3]
                _valid_identifier(identifier1)
                _valid_identifier(identifier2)

                token_list.append((TokenNameEnum.IDENTIFIER, identifier1))
                token_list.append((TokenNameEnum.IDENTIFIER, identifier2))
            else:
                if number_of_strings != 3:
                    raise InvalidMYQASMSyntaxError(
                        f"`{a} {keyword}` must be followed by 1 identifier"
                    )
                identifier1 = string_list[2]
                _valid_identifier(identifier1)

                token_list.append((TokenNameEnum.IDENTIFIER, identifier1))

    return token_list
