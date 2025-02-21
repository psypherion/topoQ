"""
Example usage of the topoQ library.
Demonstrates circuit construction, visualization, simulation,
and variational optimization.
"""

import numpy as np
from topoQ.qubit import Tetron
from topoQ.gates import BraidingGate, CliffordGate
from topoQ.circuit import Circuit
from topoQ.error_model import DepolarizingNoise, AssignmentError
from topoQ.simulation import Simulation
from topoQ.visualization import draw_circuit, draw_bloch_sphere, interactive_circuit_view
from topoQ.transpiler import circuit_to_json
from topoQ.optimizer import optimize_circuit
from topoQ.var_algo import variational_optimization, vqe_stub
from typing import List

def circuit_template(params: List[float]) -> Circuit:
    theta = params[0]
    circuit = Circuit()
    circuit.add_qubit(Tetron(use_density_matrix=True))
    braid_gate = BraidingGate(theta=theta, generator="X")
    circuit.apply_gate(braid_gate, qubit_index=0)
    h_gate = CliffordGate("H")
    circuit.apply_gate(h_gate, qubit_index=0)
    circuit.measure(0, basis="Z")
    return circuit

def cost_function(circuit: Circuit) -> float:
    sim = Simulation(circuit=circuit)
    results = sim.run(shots=100)
    p1 = sum(count for key, count in results.items() if key[0] == 1) / 100.0
    return p1

def main() -> None:
    tetron = Tetron(use_density_matrix=True)
    circuit = Circuit()
    circuit.add_qubit(tetron)
    braid_gate = BraidingGate(theta=np.pi/4, generator="X")
    circuit.apply_gate(braid_gate, qubit_index=0)
    h_gate = CliffordGate("H")
    circuit.apply_gate(h_gate, qubit_index=0)
    circuit.measure(0, basis="Z")

    print("Visualizing circuit...")
    draw_circuit(circuit)

    print("Displaying Bloch sphere for the qubit...")
    draw_bloch_sphere(tetron)

    json_repr = circuit_to_json(circuit)
    print("Circuit JSON representation:")
    print(json_repr)

    optimized_circuit = optimize_circuit(circuit)
    print("Optimized circuit visualization:")
    draw_circuit(optimized_circuit)

    noise = DepolarizingNoise(p=0.02)
    assign_error = AssignmentError(p_a=0.05)
    sim = Simulation(circuit=circuit, noise_model=noise, assign_error_model=assign_error)
    results = sim.run(shots=1024)
    print("Measurement Histogram:", results)

    init_params = [np.pi/4]
    opt_params = variational_optimization(circuit_template, cost_function, init_params,
                                          learning_rate=0.1, max_iter=50)
    print("Optimized parameter:", opt_params)

    opt_params_vqe, energy = vqe_stub(None, circuit_template, init_params,
                                      learning_rate=0.1, max_iter=50)
    print("VQE stub: optimized parameter:", opt_params_vqe, "Estimated energy (stub):", energy)

    print("Interactive circuit view (stub):")
    interactive_circuit_view(circuit)

if __name__ == "__main__":
    main()
