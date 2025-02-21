"""
Defines stabilizer operators and stabilizer codes.
"""

import numpy as np
from typing import List
from .utils import kron, pauli_operator


class Stabilizer:
    """
    Represents a stabilizer operator defined on selected qubits.
    """

    def __init__(self, qubit_indices: List[int], paulis: List[str]) -> None:
        if len(qubit_indices) != len(paulis):
            raise ValueError("qubit_indices and paulis must have equal length.")
        self.qubit_indices: List[int] = qubit_indices
        self.paulis: List[str] = paulis
        self.operator: np.ndarray = self.build_operator()

    def build_operator(self) -> np.ndarray:
        total_qubits: int = max(self.qubit_indices) + 1
        op_list = []
        for i in range(total_qubits):
            if i in self.qubit_indices:
                idx = self.qubit_indices.index(i)
                op_list.append(pauli_operator(self.paulis[idx]))
            else:
                op_list.append(np.eye(2, dtype=complex))
        return kron(op_list)

    def measure(self, state: np.ndarray) -> complex:
        """
        Compute the expectation value ⟨state|S|state⟩.
        """
        return np.vdot(state, self.operator @ state)

    def __str__(self) -> str:
        return f"Stabilizer(qubits={self.qubit_indices}, paulis={self.paulis})"


class StabilizerCode:
    """
    Represents a stabilizer code over a set of qubits.
    Provides syndrome extraction.
    """

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits: int = num_qubits
        self.stabilizers: List[Stabilizer] = []

    def add_stabilizer(self, stabilizer: Stabilizer) -> None:
        self.stabilizers.append(stabilizer)

    def measure_syndrome(self, state: np.ndarray) -> List[int]:
        syndrome: List[int] = []
        for stab in self.stabilizers:
            exp_val = stab.measure(state)
            outcome = 0 if np.real(exp_val) > 0 else 1
            syndrome.append(outcome)
        return syndrome

    def simulate_syndrome_round(self, state: np.ndarray) -> List[int]:
        return self.measure_syndrome(state)

    def __str__(self) -> str:
        return f"StabilizerCode({self.num_qubits} qubits, {len(self.stabilizers)} stabilizers)"
