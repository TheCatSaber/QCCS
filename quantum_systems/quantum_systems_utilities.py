import math

from complex_matrices import (
    ComplexMatrix,
    complex_matrix_add,
    complex_matrix_multiply,
    identity,
)
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector, complex_vector_inner_product
from shared import (
    complex_matrix_eigenvalues,
    complex_matrix_eigenvectors,
    complex_matrix_vector_multiply,
)


def state_probability(ket: ComplexVector, node: int) -> float:
    if node < 0 or node >= len(ket):
        raise ValueError(
            "node must be between 0 and n-1, where n is the length of the ket."
        )
    return ket[node].modulus_squared() / ket.norm_squared()


def transition_amplitude(ket1: ComplexVector, ket2: ComplexVector) -> ComplexNumber:
    if len(ket1) != len(ket2):
        raise ValueError("Transitioning kets must be of the same length.")
    inner_product = complex_vector_inner_product(ket2, ket1)
    norms_multiplied = ket1.norm() * ket2.norm()
    norms_multiplied_as_complex = ComplexNumber(norms_multiplied, 0)
    return inner_product / norms_multiplied_as_complex


def observable_mean(matrix: ComplexMatrix, ket: ComplexVector) -> ComplexNumber:
    if not matrix.is_hermitian():
        raise ValueError("Matrix corresponding to the observable must be hermitian.")

    if len(ket) != matrix.get_height():
        raise ValueError("Improperly sized ket vector.")

    return complex_vector_inner_product(
        complex_matrix_vector_multiply(matrix, ket), ket
    )


def observable_variance(matrix: ComplexMatrix, ket: ComplexVector) -> ComplexNumber:
    expectation = observable_mean(matrix, ket)

    Delta = complex_matrix_add(
        matrix, identity(len(ket)).scalar_multiplication(expectation.inverse())
    )

    Delta_squared = complex_matrix_multiply(Delta, Delta)

    # Variance = E((X-m)^2), where m is the mean.
    # Delta = X - m
    # Delta_squared = (X -m)^2
    # So do E(Delta_squared), with respect to ket.
    return observable_mean(Delta_squared, ket)


def probability_of_each_eigenstate(
    matrix: ComplexMatrix, ket: ComplexVector
) -> list[float]:
    eigenvalues = complex_matrix_eigenvalues(matrix)
    eigenvectors = complex_matrix_eigenvectors(matrix)
    normalized_eigenvectors: list[ComplexVector] = []
    for eigenvector in eigenvectors:
        norm = eigenvector.norm()
        normalized_eigenvector = [c / norm for c in eigenvector]
        normalized_eigenvectors.append(ComplexVector(normalized_eigenvector))

    for lambda_, eigenvector in zip(eigenvalues, normalized_eigenvectors):
        assert complex_matrix_vector_multiply(matrix, eigenvector) == eigenvector.scalar_multiplication(
            lambda_
        )

    probabilities: list[float] = []
    for eigenvector in normalized_eigenvectors:
        p = complex_vector_inner_product(eigenvector, ket).modulus_squared()
        probabilities.append(p)

    assert math.isclose(sum(probabilities), 1, abs_tol=1e-8)

    mean_this_way = ComplexNumber(0, 0)

    for lambda_, p in zip(eigenvalues, probabilities):
        mean_this_way += lambda_ * p

    assert observable_mean(matrix, ket) == mean_this_way

    return probabilities
