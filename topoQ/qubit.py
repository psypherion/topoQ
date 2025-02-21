"""
Defines the Tetron class for topological qubits.
"""

import numpy as np
from typing import Optional
from .utils import pauli_operator


class Tetron:
    """
    Represents a two-sided tetron qubit encoded in four Majorana zero modes.
    The qubit is represented as a state vector by default,
    with an option for a density matrix representation.
    
    Conventions:
      Z = i * γ1 * γ2 = i * γ3 * γ4, and
      X = i * γ1 * γ3 = -i * γ2 * γ4.
      
    |0> is the +1 eigenstate of Z; |1> is the -1 eigenstate.
    """

    def __init__(self, use_density_matrix: bool = False) -> None:
        self.use_dm: bool = use_density_matrix
        self.state: np.ndarray = np.array([1, 0], dtype=complex)
        self.dm: Optional[np.ndarray] = (
            np.outer(self.state, self.state.conj()) if self.use_dm else None
        )
        self.history: list = []

    def apply_single_qubit_gate(self, gate_matrix: np.ndarray) -> None:
        """Apply a single-qubit unitary gate."""
        if self.use_dm and self.dm is not None:
            self.dm = gate_matrix @ self.dm @ gate_matrix.conj().T
            eigenvals, eigenvecs = np.linalg.eig(self.dm)
            self.state = eigenvecs[:, np.argmax(np.abs(eigenvals))]
        else:
            self.state = gate_matrix @ self.state
        self.history.append(("gate", gate_matrix))

    def measure(self, basis: str = "Z") -> int:
        """
        Simulate a projective measurement in the given basis ("Z" or "X").
        Returns the outcome (0 or 1).
        """
        if basis.upper() == "Z":
            probs = np.abs(self.state) ** 2
            outcome = int(np.random.choice([0, 1], p=probs))
            proj = np.array([1, 0], dtype=complex) if outcome == 0 else np.array([0, 1], dtype=complex)
        elif basis.upper() == "X":
            state_x = np.array(
                [(self.state[0] + self.state[1]) / np.sqrt(2),
                 (self.state[0] - self.state[1]) / np.sqrt(2)],
                dtype=complex
            )
            probs = np.abs(state_x) ** 2
            outcome = int(np.random.choice([0, 1], p=probs))
            proj = (np.array([1, 1], dtype=complex) / np.sqrt(2)
                    if outcome == 0 else np.array([1, -1], dtype=complex) / np.sqrt(2))
        else:
            raise ValueError("Unsupported basis. Choose 'X' or 'Z'.")
        self.state = proj
        if self.use_dm:
            self.dm = np.outer(self.state, self.state.conj())
        self.history.append(("measure", basis, outcome))
        return outcome

    def reset(self) -> None:
        """Reset the tetron to |0>."""
        self.state = np.array([1, 0], dtype=complex)
        if self.use_dm:
            self.dm = np.outer(self.state, self.state.conj())
        self.history.append(("reset",))

    def __str__(self) -> str:
        return f"Tetron(state={self.state}, use_dm={self.use_dm})"
