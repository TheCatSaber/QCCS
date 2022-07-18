from complex_numbers import ComplexNumber, complex_number_divide
from complex_vectors import ComplexVector, complex_vector_inner_product
from user_interaction_shared import (
    get_float,
    get_non_negative_int,
    get_positive_int,
    less_than,
)

SIZE_LIMIT = 100


def main():
    number_of_points = less_than(get_positive_int, SIZE_LIMIT)(
        "Enter the number of points (n) on the line: "
    )
    psi = ComplexVector(
        [
            ComplexNumber(
                get_float(f"Enter real part of the amplitude for x{i}: "),
                get_float(f"Enter imaginary part of the amplitude for x{i}: "),
            )
            for i in range(number_of_points)
        ]
    )
    point_to_get = less_than(get_non_negative_int, number_of_points)(
        "Enter the number of the point you wish to get (0 to n-1): "
    )
    print(round(psi[point_to_get].modulus_squared() / (psi.norm() ** 2), 8))

    print("Now getting values for the second ket.")
    psi2 = ComplexVector(
        [
            ComplexNumber(
                get_float(f"Enter real part of the amplitude for x{i}: "),
                get_float(f"Enter imaginary part of the amplitude for x{i}: "),
            )
            for i in range(number_of_points)
        ]
    )
    transition_amplitude = complex_number_divide(
        complex_vector_inner_product(psi2, psi),
        ComplexNumber(psi.norm() * psi2.norm(), 0),
    )
    rounded_amplitude = ComplexNumber(
        round(transition_amplitude.get_real(), 8),
        round(transition_amplitude.get_imaginary(), 8),
    )
    print(f"Transition amplitude: {rounded_amplitude}.")
    print(
        f"Transition probability: {round(transition_amplitude.modulus_squared(), 8)}."
    )


if __name__ == "__main__":
    main()
