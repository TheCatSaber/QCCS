import math
import random

import cirq
import numpy as np

n = 6

number_position = random.randrange(0, 2**n)
expected_answer = bin(number_position)


class MagicGate(cirq.Gate):  # type: ignore
    def __init__(self):
        super(MagicGate, self)

    def _num_qubits_(self) -> int:
        return n + 1

    def _unitary_(self):
        blank = np.array(
            [
                [1.0 if i == j else 0.0 for i in range(2 ** (n + 1))]
                for j in range(2 ** (n + 1))
            ]
        )
        blank[number_position * 2][number_position * 2] = 0.0
        blank[number_position * 2][number_position * 2 + 1] = 1.0
        blank[number_position * 2 + 1][number_position * 2] = 1.0
        blank[number_position * 2 + 1][number_position * 2 + 1] = 0.0
        return blank

    def _circuit_diagram_info_(self, _):
        return ["Uf"] * self.num_qubits()


class InversionAboutMean(cirq.Gate):  # type: ignore
    def __init__(self) -> None:
        super(InversionAboutMean, self)

    def _num_qubits_(self) -> int:
        return n

    def _unitary_(self):
        return np.array(
            [
                [2 / (2**n) - 1 if i == j else 2 / (2**n) for i in range(2**n)]
                for j in range(2**n)
            ]
        )

    def _circuit_diagram_info_(self, _):
        return ["-I + 2A"] * self.num_qubits()


magic_gate = MagicGate()
inversion_about_the_mean = InversionAboutMean()

circuit = cirq.Circuit()  # type: ignore
qubits = cirq.LineQubit.range(n + 1)  # type: ignore


for i in range(n):
    circuit.append(cirq.H(qubits[i]))  # type: ignore

circuit.append(cirq.X(qubits[n]))  # type: ignore
circuit.append(cirq.H(qubits[n]))  # type: ignore
for i in range(math.floor(math.pi / 4 * math.sqrt(2**n))):
    circuit.append(magic_gate.on(*qubits))
    circuit.append(inversion_about_the_mean.on(*qubits[:n]))

circuit.append(cirq.measure(*qubits[:n]))  # type: ignore

# print(circuit)

sim = cirq.Simulator()  # type: ignore
res = sim.run(circuit)

print(res)
print(f"Expected answer is {expected_answer}")
