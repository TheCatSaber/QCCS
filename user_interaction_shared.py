from typing import Callable

from complex_numbers import ComplexNumber


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
