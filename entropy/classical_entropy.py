import math
from typing import NamedTuple, TypeAlias


class SymbolProbability(NamedTuple):
    symbol: str
    probability: float


ClassicalPDF: TypeAlias = list[SymbolProbability]


def verify_classical_pdf(PDF: ClassicalPDF) -> None:
    if not math.isclose(sum(x.probability for x in PDF), 1):
        raise ValueError("Sum of probabilities is not 1 in PDF.")
    if len(set(x.symbol for x in PDF)) != len(PDF):
        raise ValueError("Repeated symbol in PDF.")


def Shannon_entropy(PDF: ClassicalPDF) -> float:
    verify_classical_pdf(PDF)
    return sum(
        0 if x.probability == 0 else -x.probability * math.log2(x.probability)
        for x in PDF
    )
