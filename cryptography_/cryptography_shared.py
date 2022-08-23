import random
from typing import Literal, TypeAlias

Bit: TypeAlias = Literal[0] | Literal[1]
BitString: TypeAlias = list[Bit]


def random_bit_string(length: int) -> BitString:
    return [random.choice([0, 1]) for _ in range(length)]
