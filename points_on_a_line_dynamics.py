import math
from functools import reduce

from complex_matrices import ComplexMatrix, tensor_product
from complex_vectors import ComplexVector, complex_vector_tensor_product
from quantum_systems import state_probability
from shared import complex_matrix_vector_multiply
from user_interaction_shared import (
    get_complex_vector,
    get_reasonable_positive_int,
    print_vector,
    yes_no_question,
    get_sequence_of_unitary_matrices,
)


def main():
    number_of_lines = get_reasonable_positive_int("Enter the number of lines: ")
    if number_of_lines == 1:
        one_point()
    else:
        multiple_points(number_of_lines)


def one_point() -> None:
    number_of_points = get_reasonable_positive_int(
        "Enter the number of points on the line: "
    )
    print("Getting initial state vector.")
    initial_state = get_complex_vector(number_of_points)
    time_steps = get_reasonable_positive_int("Enter the number of timestamps: ")
    sequence_of_matrices = get_sequence_of_unitary_matrices(
        time_steps, number_of_points
    )

    current_state = initial_state
    for i in range(time_steps):
        current_state = complex_matrix_vector_multiply(
            sequence_of_matrices[i], current_state
        )

    print_information(
        initial_state, current_state, 1, [number_of_points], number_of_points
    )


def multiple_points(number_of_lines: int) -> None:
    number_of_points_list = [
        get_reasonable_positive_int(f"Enter the number of points on line {i}: ")
        for i in range(number_of_lines)
    ]

    size_of_tensor_space = math.prod(number_of_points_list)

    initial_state = get_initial_state(
        number_of_lines, number_of_points_list, size_of_tensor_space
    )

    time_steps = get_reasonable_positive_int("Enter the number of timestamps: ")

    sequence_of_matrices = get_sequence_of_matrices(
        number_of_lines, number_of_points_list, size_of_tensor_space, time_steps
    )

    current_state = initial_state
    for i in range(time_steps):
        current_state = complex_matrix_vector_multiply(
            sequence_of_matrices[i], current_state
        )

    print_information(
        initial_state,
        current_state,
        number_of_lines,
        number_of_points_list,
        size_of_tensor_space,
    )


def get_initial_state(
    number_of_lines: int, number_of_points_list: list[int], size_of_tensor_space: int
) -> ComplexVector:
    if yes_no_question(f"Are the {number_of_lines} lines initially entangled? (Y/N) "):
        print("Getting initial state vector for the entangled state.")
        return get_complex_vector(
            size_of_tensor_space, message="part of the entangled state index"
        )
    else:
        initial_states: list[ComplexVector] = []
        for i in range(number_of_lines):
            print(f"Getting initial state for line {i}.")
            initial_states.append(
                get_complex_vector(
                    number_of_points_list[i],
                    f"part of the amplitude for line {i} position",
                )
            )
        return reduce(complex_vector_tensor_product, initial_states)


def get_sequence_of_matrices(
    number_of_lines: int,
    number_of_points_list: list[int],
    size_of_tensor_space: int,
    time_steps: int,
) -> list[ComplexMatrix]:
    if yes_no_question("Are any of the unitary operations entangling? (Y/N) "):
        return get_sequence_of_unitary_matrices(
            time_steps,
            size_of_tensor_space,
        )
    else:
        line_matrices_list = [
            get_sequence_of_unitary_matrices(
                time_steps,
                number_of_points_list[line_number],
                message=f"Matrices for line {line_number}: matrix number",
            )
            for line_number in range(number_of_lines)
        ]
        return [
            reduce(
                tensor_product,
                [
                    line_matrices[time_step]
                    for time_step in range(time_steps)
                ],
            )
            for line_matrices in line_matrices_list
        ]


def print_information(
    initial_state: ComplexVector,
    end_state: ComplexVector,
    number_of_lines: int,
    number_of_points_list: list[int],
    size_of_tensor_space: int,
) -> None:
    print("Initial state vector.")
    print_vector(initial_state)

    print("Resulting state vector.")
    print_vector(end_state)

    print(
        "Resulting probabilities, with states of systems (when measured in the"
        " canonical bases)."
    )

    line_string = "\t".join(f"Line{i}" for i in range(number_of_lines))

    print(f"{line_string}\tP(state)")
    for i in range(size_of_tensor_space):
        values: list[int] = []
        for j in range(number_of_lines):
            if j == number_of_lines - 1:
                values.append(i % number_of_points_list[j])
            else:
                values.append(
                    (i // math.prod(number_of_points_list[j + 1 :]))
                    % number_of_points_list[j]
                )

        values_string = "\t".join(f"{j}" for j in values)
        print(f"{values_string}\t{state_probability(end_state, i)}")


if __name__ == "__main__":
    main()
