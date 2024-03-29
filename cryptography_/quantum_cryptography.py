import random
from typing import NamedTuple

from .cryptography_shared import Bit, BitString, random_bit_string


class AliceAnswer(NamedTuple):
    bit_sent: BitString
    sending_basis: BitString


class BobAnswer(NamedTuple):
    receiving_basis: BitString


class KnuthAnswer(NamedTuple):
    bit_received: BitString
    proportion_correct: float
    proportion_measured_in_same_basis: float


class Alice92Answer(NamedTuple):
    bit_sent: BitString


def alice(n: int) -> AliceAnswer:
    return AliceAnswer(
        bit_sent=random_bit_string(n), sending_basis=random_bit_string(n)
    )


def bob(n: int) -> BobAnswer:
    return BobAnswer(receiving_basis=random_bit_string(n))


def knuth(alice_answer: AliceAnswer, bob_answer: BobAnswer) -> KnuthAnswer:
    bit_received: BitString = []
    measured_same_count = 0
    same_basis_count = 0
    for sending_basis, receiving_basis, bit_sent in zip(
        alice_answer.sending_basis, bob_answer.receiving_basis, alice_answer.bit_sent
    ):
        if same_basis := (sending_basis == receiving_basis):
            same_basis_count += 1
        bit_measured: Bit = bit_sent if same_basis else random.choice([0, 1])
        if bit_measured == bit_sent:
            measured_same_count += 1
        bit_received.append(bit_measured)

    number_bits = len(bit_received)
    return KnuthAnswer(
        bit_received=bit_received,
        proportion_correct=(measured_same_count / number_bits),
        proportion_measured_in_same_basis=(same_basis_count / number_bits),
    )


def knuth2(alice_answer: AliceAnswer, bob_answer: BobAnswer) -> BitString:
    answer: BitString = []
    for sending_basis, receiving_basis, bit_sent in zip(
        alice_answer.sending_basis, bob_answer.receiving_basis, alice_answer.bit_sent
    ):
        if sending_basis == receiving_basis:
            answer.append(bit_sent)
    return answer


def alice92(n: int) -> Alice92Answer:
    return Alice92Answer(bit_sent=random_bit_string(n))


def bob92(n: int) -> BobAnswer:
    return bob(n)


def knuth92(alice_answer: Alice92Answer, bob_answer: BobAnswer) -> BitString:
    # Alice 0 means sent as →; 1 means sent as ↗
    # Bob 0 means measured in +; 1 means measured in X
    answer: BitString = []
    for bit_sent, receiving_basis in zip(
        alice_answer.bit_sent, bob_answer.receiving_basis
    ):
        if bit_sent == 0 and receiving_basis == 0:
            # Bob measures →
            # Bob doesn't know
            pass
        elif bit_sent == 1 and receiving_basis == 0:
            # Bob measures ↑ or → (50/50)
            # ↑ means Bob is certain it is 1.
            # Otherwise Bob doesn't know
            if random.choice([0, 1]) == 0:
                # Ignore the lines, as they occur randomly
                answer.append(1)  # pragma: no cover
        elif bit_sent == 0 and receiving_basis == 1:
            # Bob measures ↗ or ↘ (50/50)
            # ↘ means Bob is certain it is 0.
            # Otherwise Bob doesn't know
            if random.choice([0, 1]) == 0:
                # Ignore the lines, as they occur randomly
                answer.append(0)  # pragma: no cover
        elif bit_sent == 1 and receiving_basis == 1:
            # Bob measures ↗
            # Bob doesn't know
            pass
    return answer
