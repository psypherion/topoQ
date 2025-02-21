"""
Simulation engine for topoQ circuits.
"""

from typing import Dict, Any, List
import numpy as np
from .circuit import Circuit
from .error_model import AssignmentError, DepolarizingNoise
from tqdm import tqdm


class Simulation:
    """
    Simulation engine to run a circuit over multiple shots.
    Supports a "statevector" backend (default) and stubs for density matrix simulation.
    """

    def __init__(
        self,
        circuit: Circuit,
        noise_model: Any = None,
        assign_error_model: Any = None,
        backend: str = "statevector",
    ) -> None:
        self.circuit: Circuit = circuit
        self.noise_model: Any = noise_model
        self.assign_error_model: Any = assign_error_model
        self.backend: str = backend

    def run(self, shots: int = 1024) -> Dict[Any, int]:
        results: List[dict] = []
        for _ in tqdm(range(shots), desc="Running simulation shots"):
            self.circuit.clear_operations()
            shot_result = self.circuit.run()
            if self.assign_error_model is not None:
                for qubit in shot_result:
                    shot_result[qubit] = self.assign_error_model.apply(shot_result[qubit])
            results.append(shot_result)
        return self.aggregate_results(results)

    def aggregate_results(self, results: List[dict]) -> Dict[Any, int]:
        histogram: Dict[Any, int] = {}
        for shot in results:
            key = tuple(shot.get(i, None) for i in range(len(self.circuit.qubits)))
            histogram[key] = histogram.get(key, 0) + 1
        return histogram


def run_density_matrix_simulation(circuit: Circuit, shots: int = 1024) -> Dict[Any, int]:
    """
    Stub for density matrix simulation.
    """
    sim = Simulation(circuit, backend="density_matrix")
    return sim.run(shots=shots)
