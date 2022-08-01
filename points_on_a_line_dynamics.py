from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber
from quantum_systems import state_probability
from shared import complex_matrix_vector_multiply
from user_interaction_shared import (
    get_complex_vector,
    get_float,
    print_vector,
    get_reasonable_positive_int,
)


def main():
    number_of_points = get_reasonable_positive_int(
        "Enter the number of points (n) on the line: "
    )
    print("Getting initial state vector.")
    psi = get_complex_vector(number_of_points)
    time_steps = get_reasonable_positive_int("Enter the number of timestamps (n2): ")
    sequence_of_matrices: list[ComplexMatrix] = []
    for i in range(time_steps):
        while True:
            print(f"\nGetting unitary matrix number {i}.")
            matrix: list[list[ComplexNumber]] = []
            for row_number in range(number_of_points):
                row: list[ComplexNumber] = [
                    ComplexNumber(
                        get_float(
                            "Enter real part of the amplitude for row"
                            f" {row_number} column {column_number}: "
                        ),
                        get_float(
                            "Enter imaginary part of the amplitude for row"
                            f" {row_number} column {column_number}: "
                        ),
                    )
                    for column_number in range(number_of_points)
                ]
                matrix.append(row)
            m = ComplexMatrix(matrix)
            if not m.is_unitary():
                print("You did not enter a unitary matrix. Please try again:")
            else:
                sequence_of_matrices.append(m)
                break

    current_state = psi
    for i in range(time_steps):
        current_state = complex_matrix_vector_multiply(
            sequence_of_matrices[i], current_state
        )

    print("Resulting state vector.")
    print_vector(current_state)

    print("Resulting probabilities (when measured in the canonical bases).")

    print("[")
    for i in range(number_of_points):
        print(f"\t{state_probability(current_state, i)}")
    print("]")


if __name__ == "__main__":
    main()
