import itertools
from cryptography_ import BitString

from .classical_entropy import ClassicalPDF, verify_classical_pdf


def typical_sequences(PDF: ClassicalPDF, n: int) -> list[BitString]:
    verify_classical_pdf(PDF)
    if len(PDF) != 2 or {PDF[0].symbol, PDF[1].symbol} != {"0", "1"}:
        raise ValueError("PDF for typical sequence must be for 0 and 1")

    if n <= 0:
        raise ValueError("Number of sequences required must be at least 1")

    index_of_zero = 0 if PDF[0].symbol == "0" else 1

    no_zeros = int(round(PDF[index_of_zero].probability * n, 0))

    positions = itertools.combinations(range(n), no_zeros)
    sequences: list[BitString] = []
    for pos in positions:
        this_sequence: BitString = [0 if i in pos else 1 for i in range(n)]
        sequences.append(this_sequence)

    return sequences
