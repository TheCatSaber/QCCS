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


def get_complex_vector(n: int) -> ComplexVector:
    """Gets a complex vector of size n from the user."""
    return ComplexVector(
        [
            ComplexNumber(
                get_float(f"Enter real part of the amplitude for x{i}: "),
                get_float(f"Enter imaginary part of the amplitude for x{i}: "),
            )
            for i in range(n)
        ]
    )


SIZE_LIMIT = 100

get_reasonable_positive_int: Callable[[str], int] = less_than(
    get_positive_int, SIZE_LIMIT
)
