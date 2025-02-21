"""
Optimizer module for topoQ.
Merges consecutive single-qubit gates using a simple heuristic.
"""

import numpy as np
from typing import Any
from .gates import GenericGate


def optimize_circuit(circuit: Any) -> Any:
    """
    Optimizes the circuit by merging consecutive single-qubit gate operations
    on the same qubit. If adjacent gates exist, their matrices are multiplied.
    Identity operations are removed.
    """
    new_ops = []
    ops = circuit.operations
    i = 0
    while i < len(ops):
        if ops[i][0] == "gate":
            qubit_idx = ops[i][1]
            merged_matrix = ops[i][2].matrix()
            j = i + 1
            while j < len(ops) and ops[j][0] == "gate" and ops[j][1] == qubit_idx:
                merged_matrix = ops[j][2].matrix() @ merged_matrix
                j += 1
            if not np.allclose(merged_matrix, np.eye(2)):
                new_gate = GenericGate(merged_matrix)
                new_ops.append(("gate", qubit_idx, new_gate))
            i = j
        else:
            new_ops.append(ops[i])
            i += 1
    circuit.operations = new_ops
    return circuit
