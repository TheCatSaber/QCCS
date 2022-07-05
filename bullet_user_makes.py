import math

from complex_matrices import ComplexMatrix, complex_matrix_multiply
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector
from marble_game import ProbabilisticMarbleGame

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)


def get_positive_int(question: str) -> int:
    while True:
        user_input = input(question)
        if not user_input.isdigit() or (user_input := int(user_input)) == 0:
            continue
        return user_input


def get_float_in_range_inclusive(
    question: str, lower_bound: float, upper_bound: float
) -> float:
    while True:
        user_input = input(question)
        try:
            user_input = float(user_input)
        except TypeError:
            continue
        if lower_bound <= user_input <= upper_bound:
            return user_input


slits: int = get_positive_int("Enter number of slits: ")
targets: int = get_positive_int("Enter number of targets: ")

nodes = slits + targets + 1  # + 1 for starting node

matrix: list[list[ComplexNumber]] = []

# Starting point can never be reached.
matrix.append([zero for _ in range(nodes)])

# Each slit has an equal probability of (1 / slits) of being selected, from the starting node.
# And cannot be reached from anywhere else.

row_p = 1 / slits

slit_row: list[ComplexNumber] = [ComplexNumber(row_p, 0)]
for _ in range(nodes - 1):
    slit_row.append(zero)
for _ in range(slits):
    matrix.append(slit_row)

# Get user's probability for each slit.
all_slits_probabilities: list[list[float]] = []
for slit in range(1, slits + 1):
    print(f"slit {slit}")
    while True:
        this_slits_probabilities: list[float] = []
        for target in range(1, targets + 1):
            this_slits_probabilities.append(
                get_float_in_range_inclusive(
                    f"Enter the probability of going from slit {slit} to target"
                    f" {target}: ",
                    0,
                    1,
                )
            )
        if math.isclose(sum(this_slits_probabilities), 1, abs_tol=1e-8):
            all_slits_probabilities.append(this_slits_probabilities)
            break
        print("The sum of the probabilities was not 1 (to ~8d.p.)")


# Add to big matrix. Each row
# Start with a zero, as cannot be reached from the start
# Then add the complex version of each probability: which are indexed differently
# from how created
# Then add 1 one along the diagonal, with the rest 0.
for target_number in range(targets):
    row: list[ComplexNumber] = [zero]
    for slit_number in range(slits):
        row.append(
            ComplexNumber(all_slits_probabilities[slit_number][target_number], 0)
        )
    for _ in range(targets):
        row.append(zero)
    location_of_one = 1 + slits + target_number
    row[location_of_one] = one
    matrix.append(row)

b = ComplexMatrix(matrix)
b_squared = complex_matrix_multiply(b, b)

string_representation = [[str(i) for i in b.get_row(j)] for j in range(b.get_height())]
for row_ in string_representation:
    print(str(row_).replace("'", ""))

print("\n\n")

string_representation2 = [
    [str(i) for i in b_squared.get_row(j)] for j in range(b_squared.get_height())
]
for row_ in string_representation2:
    print(str(row_).replace("'", ""))

initial_state = ComplexVector([one] + [zero] * (nodes - 1))

game = ProbabilisticMarbleGame(nodes, 1, initial_state, b)
state_one = game.calculate_state(1)
state_two = game.calculate_state(2)

print()
string_representation3 = [str(i) for i in state_one]
print(string_representation3)
print()
string_representation4 = [str(i) for i in state_two]
print(string_representation4)

