"""
Error models for topoQ.
"""

import numpy as np
from typing import Any
from .utils import pauli_operator


class DepolarizingNoise:
    """
    Depolarizing noise channel: with probability p, applies a random Pauli error.
    """

    def __init__(self, p: float) -> None:
        self.p: float = p

    def apply(self, state: np.ndarray) -> np.ndarray:
        if np.random.rand() < self.p:
            error = np.random.choice(["X", "Y", "Z"])
            return np.dot(pauli_operator(error), state)
        return state


class AmplitudeDampingNoise:
    """
    Amplitude damping channel.
    For a state vector |ψ> = [a, b]^T, it damps the |1> amplitude.
    """

    def __init__(self, gamma: float) -> None:
        self.gamma: float = gamma

    def apply(self, state: np.ndarray) -> np.ndarray:
        E0 = np.array([[1, 0], [0, np.sqrt(1 - self.gamma)]], dtype=complex)
        E1 = np.array([[0, np.sqrt(self.gamma)], [0, 0]], dtype=complex)
        p0 = np.vdot(state, E0.conj().T @ E0 @ state).real
        p1 = np.vdot(state, E1.conj().T @ E1 @ state).real
        r = np.random.rand()
        if r < p0 and p0 > 0:
            return np.dot(E0, state) / np.sqrt(p0)
        elif p1 > 0:
            return np.dot(E1, state) / np.sqrt(p1)
        return state


class AssignmentError:
    """
    Models measurement assignment error: flips outcome with probability p_a.
    """

    def __init__(self, p_a: float) -> None:
        self.p_a: float = p_a

    def apply(self, outcome: int) -> int:
        if np.random.rand() < self.p_a:
            return 1 - outcome
        return outcome
