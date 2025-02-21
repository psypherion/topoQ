"""
Utility functions for topoQ.
"""

import numpy as np
from functools import reduce
from typing import List


def pauli_operator(op: str) -> np.ndarray:
    """
    Returns the 2x2 numpy array corresponding to the given Pauli operator.
    """
    op = op.upper()
    if op == "I":
        return np.array([[1, 0], [0, 1]], dtype=complex)
    elif op == "X":
        return np.array([[0, 1], [1, 0]], dtype=complex)
    elif op == "Y":
        return np.array([[0, -1j], [1j, 0]], dtype=complex)
    elif op == "Z":
        return np.array([[1, 0], [0, -1]], dtype=complex)
    else:
        raise ValueError("Unsupported Pauli operator. Choose from I, X, Y, Z.")


def kron(ops: List[np.ndarray]) -> np.ndarray:
    """
    Computes the Kronecker product of a list of operators.
    """
    return reduce(np.kron, ops)
