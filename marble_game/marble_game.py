import math

from complex_matrices import ComplexMatrix
from complex_numbers import ComplexNumber, complex_number_add
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

        Raises `ValueError` if anything is not valid.
        """
        self._check_nodes(nodes)
        self._check_marble_count(marble_count)
        self._check_initial_state(initial_state, nodes, marble_count)
        self._check_movement_matrix(movement_matrix, nodes)

        self.nodes = nodes
        self.marble_count = marble_count
        self.initial_state = initial_state
        self.movement_matrix = movement_matrix

    @classmethod
    def _check_nodes(cls, nodes: int) -> None:
        cls._check_positive_value(
            nodes, "Number of nodes in the Marble Game must be positive."
        )

    @classmethod
    def _check_marble_count(cls, marble_count: int) -> None:
        cls._check_positive_value(
            marble_count, "Number of marbles in the Marble Game must be positive."
        )

    @staticmethod
    def _check_positive_value(value: int, error_string: str) -> None:
        if value <= 0:
            raise ValueError(error_string)

    @classmethod
    def _check_initial_state(
        cls, initial_state: ComplexVector, nodes: int, marble_count: int
    ) -> None:
        cls._check_initial_state_type(initial_state)
        cls._check_initial_state_length(initial_state, nodes)
        cls._check_initial_state_total(initial_state, marble_count)

    @staticmethod
    def _check_initial_state_type(initial_state: ComplexVector) -> None:
        if any(not c.is_non_negative_integer() for c in initial_state):
            raise ValueError("All initial states must be positive integers.")

    @staticmethod
    def _check_initial_state_length(initial_state: ComplexVector, nodes: int) -> None:
        if len(initial_state) != nodes:
            raise ValueError("Length of initial state must be nodes.")

    @staticmethod
    def _check_initial_state_total(
        initial_state: ComplexVector, marble_count: int
    ) -> None:
        total = zero
        for count in initial_state:
            total = complex_number_add(total, count)

        if total.get_real() != marble_count:
            raise ValueError(
                "Sum of initial marbles must be equal to the marble count."
            )

    @classmethod
    def _check_movement_matrix(cls, movement_matrix: ComplexMatrix, nodes: int) -> None:
        cls._check_movement_matrix_shape_and_size(movement_matrix, nodes)
        cls._check_movement_matrix_legal_values(movement_matrix, nodes)
        cls._check_movement_matrix_column_sum(movement_matrix, nodes)

    @staticmethod
    def _check_movement_matrix_shape_and_size(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        if not movement_matrix.is_square():
            raise ValueError("movement_matrix must be a square matrix.")

        if movement_matrix.get_width() != nodes:
            raise ValueError(
                "movement_matrix's size must be equal to the number of nodes."
            )

    @staticmethod
    def _check_movement_matrix_legal_values(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        for i in range(nodes):
            if any(
                not (element == zero or element == one)
                for element in movement_matrix.get_row(i)
            ):
                raise ValueError("All values in movement_matrix must be 0 or 1.")

    @staticmethod
    def _check_movement_matrix_column_sum(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        for column_index in range(nodes):
            column_sum = zero
            for value in movement_matrix.get_column(column_index):
                column_sum = complex_number_add(column_sum, value)
            if column_sum != one:
                raise ValueError(
                    "All columns in movement_matrix must have exactly one 1."
                )

    def calculate_state(self, iterations: int) -> ComplexVector:
        if iterations < 0:
            raise ValueError("Iterations must be positive or 0.")

        new_state = self.initial_state
        for _ in range(iterations):
            new_state = complex_matrix_vector_multiply(self.movement_matrix, new_state)

        return new_state


class ProbabilisticMarbleGame(MarbleGame):
    def __init__(
        self,
        nodes: int,
        marble_count: int,
        initial_state: ComplexVector,
        movement_matrix: ComplexMatrix,
    ) -> None:
        super().__init__(nodes, marble_count, initial_state, movement_matrix)

    @staticmethod
    def _check_initial_state_type(initial_state: ComplexVector) -> None:
        if any(not c.is_non_negative_real() for c in initial_state):
            raise ValueError("All initial states must be positive reals.")

    @staticmethod
    def _check_movement_matrix_legal_values(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        for i in range(nodes):
            if any(
                not (element.is_non_negative_real()) or element.get_real() > 1
                for element in movement_matrix.get_row(i)
            ):
                raise ValueError(
                    "All values in movement_matrix must be real, between 0 and 1"
                    " (inclusive)."
                )


class QuantumMarbleGame(MarbleGame):
    def __init__(
        self,
        nodes: int,
        marble_count: int,
        initial_state: ComplexVector,
        movement_matrix: ComplexMatrix,
    ) -> None:
        super().__init__(nodes, marble_count, initial_state, movement_matrix)

    @staticmethod
    def _check_initial_state_type(initial_state: ComplexVector) -> None:
        # All numbers are valid.
        # Size will be verified by sum of moduli squared.
        pass

    @staticmethod
    def _check_initial_state_total(
        initial_state: ComplexVector, marble_count: int
    ) -> None:
        total = sum(c.modulus_squared() for c in initial_state)
        if not (math.isclose(total, marble_count, abs_tol=1e-8)):
            raise ValueError(
                "Sum of moduli squared of the initial marbles must be equal to the"
                " marble count."
            )

    @staticmethod
    def _check_movement_matrix_legal_values(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        # All numbers are valid.
        # Size will be verified by column sum.
        pass

    @staticmethod
    def _check_movement_matrix_column_sum(
        movement_matrix: ComplexMatrix, nodes: int
    ) -> None:
        for column_index in range(nodes):
            column_sum = sum(
                c.modulus_squared() for c in movement_matrix.get_column(column_index)
            )
            if not math.isclose(column_sum, 1, abs_tol=1e-8):
                raise ValueError(
                    "Sum of moduli squared of the movement_matrix columns must be equal"
                    " to 1."
                )
