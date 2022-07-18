import math

from complex_matrices import ComplexMatrix, complex_matrix_multiply
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector
from marble_game import ProbabilisticMarbleGame
from user_interaction_shared import get_float, get_positive_int

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)


def main():
    slits, targets, nodes = get_slits_targets_nodes()

    matrix = initial_matrix_creation(slits, nodes)

    # Get user's probability for each slit.
    all_slits_probabilities = get_users_probabilities(slits, targets)

    matrix = complete_matrix(slits, targets, matrix, all_slits_probabilities)

    bullet_matrix = ComplexMatrix(matrix)
    bullet_matrix_squared, after_one, after_two = perform_calculations(
        nodes, bullet_matrix
    )
    print_information_to_user(
        bullet_matrix, bullet_matrix_squared, after_one, after_two
    )


def get_slits_targets_nodes() -> tuple[int, int, int]:
    slits: int = get_positive_int("Enter number of slits: ")
    targets: int = get_positive_int("Enter number of targets: ")

    nodes = slits + targets + 1  # + 1 for starting node
    return slits, targets, nodes


def initial_matrix_creation(slits: int, nodes: int) -> list[list[ComplexNumber]]:
    # Create matrix, with all 0 starting row.
    matrix: list[list[ComplexNumber]] = [[zero] * nodes]

    return add_rows_for_slits(slits, nodes, matrix)


def add_rows_for_slits(
    slits: int, nodes: int, matrix: list[list[ComplexNumber]]
) -> list[list[ComplexNumber]]:
    # Each slit has an equal probability of (1 / slits) of being selected, from the starting node.
    # And cannot be reached from anywhere else.
    slit_probability = 1 / slits

    slit_row: list[ComplexNumber] = [ComplexNumber(slit_probability, 0)] + [zero] * (
        nodes - 1
    )
    return matrix + [slit_row] * slits


def get_users_probabilities(slits: int, targets: int) -> list[list[float]]:
    all_slits_probabilities: list[list[float]] = []
    for slit in range(1, slits + 1):
        print(f"Slit {slit}")
        all_slits_probabilities.append(
            get_slit_target_probabilities_and_check_sum(slit, targets)
        )
    return all_slits_probabilities


def get_slit_target_probabilities_and_check_sum(slit: int, targets: int) -> list[float]:
    while True:
        probabilities = get_slit_target_probabilities(slit, targets)
        if not check_sum_of_slit_target_probabilities(probabilities):
            print("The sum of the probabilities was not 1 (to ~8d.p.)")
        else:
            return probabilities


def get_slit_target_probabilities(slit: int, targets: int) -> list[float]:
    return [
        get_float_in_range_inclusive(
            f"Enter the probability of going from slit {slit} to target {target}: ",
            0,
            1,
        )
        for target in range(1, targets + 1)
    ]


def check_sum_of_slit_target_probabilities(probabilities: list[float]):
    return math.isclose(sum(probabilities), 1, abs_tol=1e-8)


def get_float_in_range_inclusive(
    question: str, lower_bound: float, upper_bound: float
) -> float:
    while True:
        user_input = get_float(question)
        if lower_bound <= user_input <= upper_bound:
            return user_input


def complete_matrix(
    slits: int,
    targets: int,
    matrix: list[list[ComplexNumber]],
    all_slits_probabilities: list[list[float]],
) -> list[list[ComplexNumber]]:
    # Add to big matrix. Each row
    # Start with a zero, as cannot be reached from the start
    # Then add the complex version of each probability:
    #     indexed with slit number, then target number.
    # Rest are 0, except for 1 along teh diagonal.
    for target_number in range(targets):
        row: list[ComplexNumber] = (
            [zero]
            + [
                ComplexNumber(all_slits_probabilities[slit_number][target_number], 0)
                for slit_number in range(slits)
            ]
            + [zero] * targets
        )
        location_of_one = 1 + slits + target_number
        row[location_of_one] = one
        matrix.append(row)
    return matrix


def perform_calculations(
    nodes: int, bullet_matrix: ComplexMatrix
) -> tuple[ComplexMatrix, ComplexVector, ComplexVector]:
    bullet_matrix_squared = complex_matrix_multiply(bullet_matrix, bullet_matrix)
    initial_state = ComplexVector([one] + [zero] * (nodes - 1))
    game = ProbabilisticMarbleGame(nodes, 1, initial_state, bullet_matrix)
    state_after_one_iteration = game.calculate_state(1)
    state_after_two_iterations = game.calculate_state(2)
    return bullet_matrix_squared, state_after_one_iteration, state_after_two_iterations


def print_information_to_user(
    bullet_matrix: ComplexMatrix,
    bullet_matrix_squared: ComplexMatrix,
    state_after_one_iteration: ComplexVector,
    state_after_two_iterations: ComplexVector,
) -> None:
    print("Original Matrix:")
    print_matrix(bullet_matrix)
    print("Matrix squared (probabilities after 2 rounds):")
    print_matrix(bullet_matrix_squared)
    print("State after one iteration, if bullet starts at the start:")
    print_vector(state_after_one_iteration)
    print("State after two iterations, if bullet starts at the start: ")
    print_vector(state_after_two_iterations)


def print_matrix(m: ComplexMatrix) -> None:
    for row_number in range(m.get_height()):
        print("[", end="")
        print(*m.get_row(row_number), sep=", \t", end="")
        print("],")


def print_vector(v: ComplexVector) -> None:
    print("[")
    for e in v:
        print(f"\t{e},")
    print("]")


if __name__ == "__main__":
    main()
