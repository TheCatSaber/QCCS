from complex_numbers import ComplexNumber, complex_number_divide
from complex_vectors import ComplexVector, complex_vector_inner_product


def state_probability(ket: ComplexVector, node: int) -> float:
    if node < 0 or node >= len(ket):
        raise ValueError(
            "node must be between 0 and n-1, where n is the length of the ket."
        )
    return ket[node].modulus_squared() / ket.norm_squared()


def transition_amplitude(ket1: ComplexVector, ket2: ComplexVector) -> ComplexNumber:
    inner_product = complex_vector_inner_product(ket2, ket1)
    norms_multiplied = ket1.norm() * ket2.norm()
    norms_multiplied_as_complex = ComplexNumber(norms_multiplied, 0)
    return complex_number_divide(inner_product, norms_multiplied_as_complex)
