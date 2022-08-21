import math
import random
from enum import Enum, auto
from typing import Optional

from complex_matrices import ComplexMatrix, tensor_product
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector

one_over_root_two = 1 / math.sqrt(2)
_hadamard_matrix = ComplexMatrix(
    [[one_over_root_two, one_over_root_two], [one_over_root_two, -one_over_root_two]]
)
_CNOT_matrix = ComplexMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

_registers: dict[str, ComplexVector] = {}
_user_defined_gates: dict[str, ComplexMatrix] = {}


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


def get_user_defined_gates():
    return _user_defined_gates


def _is_builtin_gate(identifier: str) -> bool:
    if identifier in ["H", "CNOT"]:
        return True

    elif identifier[0] == "I" and len(identifier) >= 2:
        numeric_bit = identifier[1:]
        return numeric_bit.isdigit()

    elif identifier[0] == "R" and len(identifier) >= 2:
        numeric_bit = identifier[1:]
        return all(char.isdigit() or char == "." for char in numeric_bit) and (
            numeric_bit.count(".") <= 1
        )

    else:
        return False


def _gate_exists(identifier: str) -> bool:
    return _is_builtin_gate(identifier) or identifier in _user_defined_gates.keys()


def _get_gate_matrix(identifier: str) -> ComplexMatrix:
    if not _gate_exists(identifier):
        raise InvalidMYQASMSyntaxError("Invalid gate.")
    if identifier in _user_defined_gates.keys():
        return _user_defined_gates[identifier]
    elif _is_builtin_gate(identifier):
        if identifier == "H":
            return _hadamard_matrix
        elif identifier == "CNOT":
            return _CNOT_matrix
        elif identifier[0] == "I":
            return ComplexMatrix.identity(int(identifier[1:]))
        elif identifier[0] == "R":
            return ComplexMatrix(
                [
                    [1, 0],
                    [
                        0,
                        ComplexNumber.new_from_polar(
                            1, math.pi * float(identifier[1:])
                        ),
                    ],
                ]
            )
    # This line is unreachable, as otherwise the gate would not be a valid gate,
    # and so InvalidMYQASMSyntaxError would have been raised earlier.
    raise InvalidMYQASMSyntaxError("Invalid gate.")  # pragma: no cover


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
            if _is_builtin_gate(identifier):
                raise InvalidMYQASMSyntaxError(
                    "Cannot create register with the name of a builtin gate."
                )
            v: list[int] = [1] + [0] * ((2 ** int(qubit_count)) - 1)
            if len(token_stream) == 6:
                initial_state = token_stream[4][1]
                assert isinstance(initial_state, str)
                v[0] = 0
                v[int(initial_state, 2)] = 1
            _registers[identifier] = ComplexVector(v)
            return
        case KeywordEnum.CONCAT | KeywordEnum.TENSOR:
            new_gate_name = token_stream[0][1]
            old_gate_1 = token_stream[2][1]
            old_gate_2 = token_stream[3][1]
            assert isinstance(new_gate_name, str)
            assert isinstance(old_gate_1, str)
            assert isinstance(old_gate_2, str)
            if not (_gate_exists(old_gate_1) and _gate_exists(old_gate_2)):
                error_keyword = "CONCAT" if keyword == KeywordEnum.CONCAT else "TENSOR"
                raise InvalidMYQASMSyntaxError(
                    f"Attempting to {error_keyword} gates that do not exist."
                )

            if _is_builtin_gate(new_gate_name):
                raise InvalidMYQASMSyntaxError("Attempting to redefine builtin gate.")
            if new_gate_name in _registers.keys():
                raise InvalidMYQASMSyntaxError(
                    "Attempting to redefine a user-defined register"
                )
            if keyword == KeywordEnum.CONCAT:
                try:
                    _user_defined_gates[new_gate_name] = _get_gate_matrix(
                        old_gate_1
                    ) * _get_gate_matrix(old_gate_2)
                except ValueError:
                    raise InvalidMYQASMSyntaxError(
                        "Cannot CONCAT gates that act on different number of qubits."
                    )
                return
            else:
                _user_defined_gates[new_gate_name] = tensor_product(
                    _get_gate_matrix(old_gate_1), _get_gate_matrix(old_gate_2)
                )
        case KeywordEnum.MEASURE:
            register_name = token_stream[1][1]
            assert isinstance(register_name, str)
            if register_name not in _registers.keys():
                raise InvalidMYQASMSyntaxError(
                    "Attempting to measure a register that does not exist."
                )
            vector_representing_state = _registers[register_name]
            vector_norm_squared = vector_representing_state.norm_squared()
            number_states = len(vector_representing_state)
            probabilities = [
                c.modulus_squared() / vector_norm_squared
                for c in vector_representing_state
            ]
            chosen_state_list = random.choices(
                range(number_states), weights=probabilities, k=1
            )
            chosen_state = chosen_state_list[0]
            binary_representation = bin(chosen_state).removeprefix("0b")
            number_in_binary_rep = len(binary_representation)
            extra_chars = "0" * (int(math.log(number_states, 2)) - number_in_binary_rep)
            return [int(char) for char in (extra_chars + binary_representation)]
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
