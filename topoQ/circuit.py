"""
Defines the Circuit and SubCircuit classes.
"""

from typing import List, Tuple, Union, Any
from .qubit import Tetron


class Circuit:
    """
    Represents a quantum circuit.
    Each operation is a tuple:
      ("gate", qubit_index: int, op: Any),
      ("multi_gate", qubit_indices: List[int], op: Any),
      ("measure", qubit_index: int, basis: str), or
      ("reset", qubit_index: int).
    """

    def __init__(self) -> None:
        self.qubits: List[Tetron] = []
        self.operations: List[Tuple[str, Any, Any]] = []
        self.subcircuits: List[SubCircuit] = []

    def add_qubit(self, qubit: Tetron) -> None:
        self.qubits.append(qubit)

    def apply_gate(self, gate: Any, qubit_index: int) -> None:
        self.operations.append(("gate", qubit_index, gate))

    def apply_multi_qubit_gate(self, gate: Any, qubit_indices: List[int]) -> None:
        self.operations.append(("multi_gate", qubit_indices, gate))

    def measure(self, qubit_index: int, basis: str = "Z") -> None:
        self.operations.append(("measure", qubit_index, basis))

    def reset(self, qubit_index: Union[int, None] = None) -> None:
        if qubit_index is None:
            for i in range(len(self.qubits)):
                self.operations.append(("reset", i))
        else:
            self.operations.append(("reset", qubit_index))

    def add_subcircuit(self, subcircuit: "SubCircuit") -> None:
        self.subcircuits.append(subcircuit)

    def run(self) -> dict:
        results: dict = {}
        for op in self.operations:
            if op[0] == "gate":
                self.qubits[op[1]].apply_single_qubit_gate(op[2].matrix())
            elif op[0] == "multi_gate":
                # Stub for multi-qubit gate simulation.
                indices = op[1]
                results[f"multi_{indices}"] = "Applied multi-qubit gate (stub)"
            elif op[0] == "measure":
                outcome = self.qubits[op[1]].measure(op[2])
                results[op[1]] = outcome
            elif op[0] == "reset":
                self.qubits[op[1]].reset()
        return results

    def clear_operations(self) -> None:
        self.operations = []

    def __str__(self) -> str:
        return f"Circuit({len(self.qubits)} qubits, {len(self.operations)} operations)"


class SubCircuit(Circuit):
    """
    Represents a subcircuit (a modular component of a larger circuit).
    """

    def __init__(self, label: str = "SubCircuit") -> None:
        super().__init__()
        self.label: str = label

    def __str__(self) -> str:
        return f"SubCircuit({self.label}, {len(self.qubits)} qubits, {len(self.operations)} operations)"
