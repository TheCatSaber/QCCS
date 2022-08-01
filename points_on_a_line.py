from quantum_systems import state_probability, transition_amplitude
from user_interaction_shared import (
    get_complex_vector,
    get_non_negative_int,
    get_reasonable_positive_int,
    less_than,
    rounded_complex_number,
)

SIZE_LIMIT = 100


def main():
    number_of_points = get_reasonable_positive_int(
        "Enter the number of points (n) on the line: "
    )
    psi = get_complex_vector(number_of_points)
    point_to_get = less_than(get_non_negative_int, number_of_points)(
        "Enter the number of the point you wish to get (0 to n-1): "
    )
    print(round(state_probability(psi, point_to_get), 8))

    print("Now getting values for the second ket.")
    psi2 = get_complex_vector(number_of_points)
    transition_amplitude_ = transition_amplitude(psi, psi2)
    print(f"Transition amplitude: {rounded_complex_number(transition_amplitude_)}.")
    print(
        f"Transition probability: {round(transition_amplitude_.modulus_squared(), 8)}."
    )


if __name__ == "__main__":
    main()
