"""
Defines gate classes for topoQ.
"""

import numpy as np
from typing import Any
from .utils import pauli_operator


class BraidingGate:
    """
    Implements a braiding gate: U(θ) = exp(-i θ G),
    where G is a Pauli operator (e.g., "X" or "Z").
    """

    def __init__(self, theta: float, generator: str = "X") -> None:
        self.theta: float = theta
        self.generator_name: str = generator.upper()
        self.generator: np.ndarray = pauli_operator(self.generator_name)

    def matrix(self) -> np.ndarray:
        from scipy.linalg import expm
        return expm(-1j * self.theta * self.generator)

    def __str__(self) -> str:
        return f"BraidingGate(theta={self.theta}, generator={self.generator_name})"


class CliffordGate:
    """
    Implements standard Clifford gates (e.g., "H", "S").
    """

    def __init__(self, name: str) -> None:
        self.name: str = name.upper()
        self._matrix: np.ndarray = self.get_matrix(self.name)

    def get_matrix(self, name: str) -> np.ndarray:
        if name == "H":
            return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        elif name == "S":
            return np.array([[1, 0], [0, 1j]], dtype=complex)
        else:
            raise ValueError("Unsupported Clifford gate. Use 'H' or 'S'.")

    def matrix(self) -> np.ndarray:
        return self._matrix

    def __str__(self) -> str:
        return f"CliffordGate(name={self.name})"


class TGate:
    """
    Represents a T gate (π/4 rotation about Z).
    """

    def __init__(self) -> None:
        self._matrix: np.ndarray = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

    def matrix(self) -> np.ndarray:
        return self._matrix

    def __str__(self) -> str:
        return "TGate()"


class GenericGate:
    """
    A generic single-qubit gate defined by a 2x2 unitary matrix.
    Useful for gate merging during optimization.
    """

    def __init__(self, matrix: np.ndarray) -> None:
        self._matrix: np.ndarray = matrix

    def matrix(self) -> np.ndarray:
        return self._matrix

    def __str__(self) -> str:
        return f"GenericGate(matrix={self._matrix})"


class CZGate:
    """
    A two-qubit Controlled-Z (CZ) gate.
    """

    def __init__(self) -> None:
        self._matrix: np.ndarray = np.diag([1, 1, 1, -1])

    def matrix(self) -> np.ndarray:
        return self._matrix

    def __str__(self) -> str:
        return "CZGate()"
