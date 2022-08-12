from typing import NamedTuple

from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector

from marble_game import QuantumMarbleGame

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)


class InterferenceDetectorOutput(NamedTuple):
    original: ComplexMatrix
    after_n_iterations: ComplexMatrix
    original_moduli_squared: ComplexMatrix
    after_n_iterations_moduli_squared: ComplexMatrix
    interference_locations: list[tuple[int, int]]


class InterferenceDetector:
    """You provide it with a matrix, that would work as the movement_matrix
    of a QuantumMarbleGame.

    It checks that it is valid, by creating and discarding an instance of
    QuantumMarbleGame.

    It then can be called to do n iterations, where n >= 2.

    It will identify interference, by also doing n n on the matrix
    of the moduli squared of the elements of this matrix, and comparing the
    result of this to the moduli squared of the n n of the original matrix.
    """

    def __init__(self, nodes: int, movement_matrix: ComplexMatrix) -> None:
        if nodes <= 0:
            raise ValueError("Number of nodes in InterferenceDetector must be positive")
        initial_state = [zero] * nodes
        initial_state[0] = one
        try:
            QuantumMarbleGame(nodes, 1, ComplexVector(initial_state), movement_matrix)
        except ValueError as e:
            raise ValueError(
                "Invalid movement_matrix provided to InterferenceDetector. The error"
                f' message from QuantumMarbleGame is "{e}"'
            )
        self.nodes = nodes
        self.movement_matrix = movement_matrix

    def calculate_interference(self, n: int) -> InterferenceDetectorOutput:
        """Calculate differences between classical and quantum system.

        n is the number of iterations to perform.

        Return the movement matrix, m^n, the classical version of the movement matrix (m2),
        m2^n, and a list of row, column pairs showing where the differences between
        the classical version of m^n and m2^n are.
        """
        if n < 2:
            raise ValueError(
                "There cannot be interference on 1 run, and 0 or less runs are invalid."
            )
        m = self.movement_matrix
        classical_counter_part = self.movement_matrix.moduli_squared_matrix()
        c = classical_counter_part
        for _ in range(n - 1):
            # n iterations means n-1 matrix multiplications of matrices to get the resultant matrix
            m = m * self.movement_matrix
            c = c * classical_counter_part

        difference_list: list[tuple[int, int]] = []

        m_moduli_squared = m.moduli_squared_matrix()
        for row_number in range(self.nodes):
            m_row = m_moduli_squared.get_row(row_number)
            c_row = c.get_row(row_number)
            for column_number in range(self.nodes):
                if m_row[column_number] != c_row[column_number]:
                    difference_list.append((row_number, column_number))

        return InterferenceDetectorOutput(
            self.movement_matrix,
            m,
            classical_counter_part,
            m.moduli_squared_matrix(),
            difference_list,
        )
