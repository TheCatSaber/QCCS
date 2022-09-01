import math
from typing import NamedTuple, TypeAlias
from complex_matrices import ComplexMatrix

from complex_vectors import ComplexVector, complex_vector_inner_product
from .classical_entropy import Shannon_entropy, SymbolProbability
from shared import complex_matrix_eigenvalues


class QubitProbability(NamedTuple):
    symbol: str
    qubit: ComplexVector
    probability: float


QuantumPDF: TypeAlias = list[QubitProbability]


def verify_quantum_pdf(PDF: QuantumPDF):
    if not math.isclose(sum(x.probability for x in PDF), 1):
        raise ValueError("Sum of probabilities is not 1 in PDF.")
    if len(set(x.symbol for x in PDF)) != len(PDF):
        raise ValueError("Repeated symbol in PDF.")
    if any(len(x.qubit) != 2 for x in PDF):
        raise ValueError("Non single-qubit in PDF.")
    if any(not math.isclose(x.qubit.norm(), 1) for x in PDF):
        raise ValueError("Qubit is not normalized.")


def density_operator(PDF: QuantumPDF):
    verify_quantum_pdf(PDF)
    action_on_zero = ComplexVector([0, 0])
    for x in PDF:
        action_on_zero = (
            action_on_zero
            + x.probability
            * complex_vector_inner_product(x.qubit, ComplexVector([1, 0]))
            * x.qubit
        )
    action_on_one = ComplexVector([0, 0])
    for x in PDF:
        action_on_one = (
            action_on_one
            + x.probability
            * complex_vector_inner_product(x.qubit, ComplexVector([0, 1]))
            * x.qubit
        )
    return ComplexMatrix(
        [[action_on_zero[0], action_on_one[0]], [action_on_zero[1], action_on_one[1]]]
    )


def von_Neumann_entropy(PDF: QuantumPDF) -> float:
    verify_quantum_pdf(PDF)
    D = density_operator(PDF)
    eigenvalues = complex_matrix_eigenvalues(D)
    return Shannon_entropy(
        [
            SymbolProbability("A", eigenvalues[0].get_real()),
            SymbolProbability("B", eigenvalues[1].get_real()),
        ]
    )
