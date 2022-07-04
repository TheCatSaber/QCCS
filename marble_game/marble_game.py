from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber
from complex_vectors import ComplexVector
from shared import complex_matrix_vector_multiply

zero = ComplexNumber(0, 0)
one = ComplexNumber(1, 0)


class MarbleGame:
    def __init__(
        self,
        nodes: int,
        marble_count: int,
        initial_state: ComplexVector,
        movement_matrix: ComplexMatrix,
    ) -> None:
        """Create marble game.

        `nodes`: number of nodes (`int`).
        `marble_count`: number of marbles to start with (`int`).
        `initial_state`: initial distribution of marbles (`ComplexVector`),
        where each element is an integer.
        Sum of initial states must be `marble_count`.
        Length must be `nodes`.
        `movement_matrix`: how marbles move (`ComplexMatrix`).
        There must be exactly one
        `1` per column, everything else must be `0`.
        """
        # Check positive values of nodes and marble_count.
        if nodes <= 0:
            raise ValueError("Must have a positive number of nodes in the MarbleGame.")

        if marble_count <= 0:
            raise ValueError(
                "Must have a positive number of marbles in the MarbleGame."
            )

        # Check positive, integer values in initial_state.
        for c in initial_state:
            c_re = c.get_real()
            c_im = c.get_imaginary()
            if c_re < 0 or int(c_re) != c_re or c_im != 0:
                raise ValueError("All initial states must be positive integers.")

        # Check length of initial state.
        if len(initial_state) != nodes:
            raise ValueError("Length of initial state must be nodes.")

        # Check initial marble count.
        total = 0
        for count in initial_state:
            total += count.get_real()

        if total != marble_count:
            raise ValueError(
                "Sum of initial marbles must be equal to the marble count."
            )

        # Check movement_matrix is square, and size equals number of nodes.
        if not movement_matrix.is_square():
            raise ValueError("movement_matrix must be a square matrix.")

        if movement_matrix.get_width() != nodes:
            raise ValueError(
                "movement_matrix's size must be equal to the number of nodes."
            )

        # Check values in movement_matrix that are 0 or 1.
        for i in range(nodes):
            if any(
                (element != zero and element != one)
                for element in movement_matrix.get_row(i)
            ):
                raise ValueError("All values in movement_matrix must be 0 or 1.")

        # Check exactly one 1 per column.
        for column_index in range(nodes):
            column_one_count = 0
            for row_index in range(nodes):
                row = movement_matrix.get_row(row_index)
                if row[column_index] == one:
                    column_one_count += 1
            if column_one_count != 1:
                raise ValueError(
                    "All columns in movement_matrix must have exactly one 1."
                )

        self.nodes = nodes
        self.marble_count = marble_count
        self.initial_state = initial_state
        self.movement_matrix = movement_matrix

    def calculate_state(self, iterations: int) -> ComplexVector:
        if iterations < 0:
            raise ValueError("Iterations must be positive or 0.")

        new_state = self.initial_state
        for _ in range(iterations):
            new_state = complex_matrix_vector_multiply(self.movement_matrix, new_state)

        return new_state
