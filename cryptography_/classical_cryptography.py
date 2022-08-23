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
