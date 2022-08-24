from typing import Literal

from .cryptography_shared import BitString, random_bit_string


def caesar_encode(plaintext: str, key: int) -> str:
    new_chars: list[str] = []
    for char in plaintext:
        char_index = ord(char)
        if char.isalpha():
            if char.isupper():
                char_offset = ord("A")
            else:
                char_offset = ord("a")
            char_index -= char_offset
            char_index += key
            char_index %= 26
            char_index += char_offset
        new_chars.append(chr(char_index))
    return "".join(new_chars)


def caesar_decode(ciphertext: str, key: int) -> str:
    return caesar_encode(ciphertext, -key)


def one_time_pad_key_gen(n: int) -> BitString:
    return random_bit_string(n)


def one_time_pad_encode(plaintext: str, key: BitString) -> str:
    if not all(ord(char) < 256 for char in plaintext):
        raise ValueError(
            "One Time Pad only supports 8-bit characters (that is, characters where"
            " ord(char) <= 255)."
        )
    if len(key) < len(plaintext) * 8:
        raise ValueError("Key is too short.")
    answer_character_list: list[str] = []
    for index, char in enumerate(plaintext):
        bin_rep = bin(ord(char)).removeprefix("0b")
        extra_chars = "0" * (8 - len(bin_rep))
        bin_rep = extra_chars + bin_rep
        bin_rep = [int(char) for char in bin_rep]
        answer_bits: list[Literal[0] | Literal[1]] = []
        for c1, c2 in zip(bin_rep, key[index * 8 : (index + 1) * 8]):
            a = c1 ^ c2
            assert a == 0 or a == 1
            answer_bits.append(a)
        bits = "0b" + "".join(str(bit) for bit in answer_bits)
        answer_character_list.append(chr(int(bits, 2)))
    return "".join(answer_character_list)


def one_time_pad_decode(ciphertext: str, key: BitString) -> str:
    return one_time_pad_encode(ciphertext, key)
