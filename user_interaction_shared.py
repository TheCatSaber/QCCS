from typing import Callable

from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector


def get_positive_int(question: str) -> int:
    while True:
        user_input = input(question)
        if not user_input.isdigit() or (user_input := int(user_input)) <= 0:
            continue
        return user_input


def get_non_negative_int(question: str) -> int:
    while True:
        user_input = input(question)
        if not user_input.isdigit() or (user_input := int(user_input)) < 0:
            continue
        return user_input


def get_float(question: str) -> float:
    while True:
        user_input = input(question)
        try:
            user_input = float(user_input)
            return user_input
        except ValueError:
            continue


def less_than(f: Callable[[str], int], limit: float):
    def wrapper(question: str):
        while True:
            a = f(question)
            if a < limit:
                return a

    return wrapper


def rounded_complex_number(c: ComplexNumber, digits: int = 8):
    return ComplexNumber(round(c.get_real(), digits), round(c.get_imaginary(), digits))


def print_matrix(m: ComplexMatrix) -> None:
    for row_number in range(m.get_height()):
        print("[", end="")
        print(*m.get_row(row_number), sep=", \t", end="")
        print("],")


def print_vector(v: ComplexVector) -> None:
    print("[")
    for e in v:
        print(f"\t{e},")
    print("]")


def get_complex_vector(
    n: int, message: str = "part of the amplitude for vector"
) -> ComplexVector:
    """Gets a complex vector of size n from the user."""
    return ComplexVector(
        [
            ComplexNumber(
                get_float(f"Enter real {message} {i}: "),
                get_float(f"Enter imaginary {message} {i}: "),
            )
            for i in range(n)
        ]
    )


def get_complex_matrix(
    width: int, height: int, message: str = "part of the amplitude for"
) -> ComplexMatrix:
    matrix: list[list[ComplexNumber]] = []
    for row_number in range(height):
        row: list[ComplexNumber] = [
            ComplexNumber(
                get_float(
                    f"Enter real {message} row {row_number} column {column_number}: "
                ),
                get_float(
                    f"Enter imaginary {message} row {row_number} column"
                    f" {column_number}: "
                ),
            )
            for column_number in range(width)
        ]
        matrix.append(row)
    return ComplexMatrix(matrix)


def yes_no_question(question: str) -> bool:
    while True:
        user_input = input(question)
        if user_input.lower() in ["y", "yes"]:
            return True
        elif user_input.lower() in ["n", "no"]:
            return False


def get_sequence_of_unitary_matrices(
    number: int,
    size: int,
    message: str = "Getting unitary matrix number",
    get_matrix_message: str = "part of the amplitude for",
) -> list[ComplexMatrix]:
    """message should allow for a space, the number of the matrix and a full stop at the end.

    Example is the default: "Getting unitary matrix number"

    get_matrix_message is the message passed to get_complex_matrix

    Example is the default: "part of the amplitude for"

    """
    matrices: list[ComplexMatrix] = []

    for i in range(number):
        while True:
            print(f"\n{message} {i}.")
            matrix = get_complex_matrix(size, size, get_matrix_message)
            if not matrix.is_unitary():
                print("You did not enter a unitary matrix. Please try again:")
            else:
                matrices.append(matrix)
                break

    return matrices


SIZE_LIMIT = 100

get_reasonable_positive_int: Callable[[str], int] = less_than(
    get_positive_int, SIZE_LIMIT
)
