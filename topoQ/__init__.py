"""
topoQ: A comprehensive simulation toolkit for topological quantum computing
using non-Abelian anyon braiding.

This package supports:
  • Topological qubits (tetrons) with optional density matrix support.
  • Various gates (braiding, Clifford, T, generic, multi-qubit CZ).
  • Circuit construction with a JSON-based IR and OpenQASM export.
  • Stabilizer codes and syndrome extraction.
  • Multiple error models and simulation backends (statevector, density matrix stubs).
  • An optimizer for gate merging and noise-aware rewrites.
  • Variational algorithm routines (VQE, QAOA stubs).
  • Enhanced visualization including circuit diagrams and Bloch sphere plotting.
  • A plugin registry and a CLI tool.
"""

from .qubit import Tetron
from .gates import BraidingGate, CliffordGate, TGate, GenericGate, CZGate
from .circuit import Circuit, SubCircuit
from .stabilizer import Stabilizer, StabilizerCode
from .measurement import perform_measurement, compute_error_metrics
from .error_model import DepolarizingNoise, AssignmentError, AmplitudeDampingNoise
from .simulation import Simulation, run_density_matrix_simulation
from .visualization import draw_circuit, draw_bloch_sphere, interactive_circuit_view
from .transpiler import circuit_to_json, circuit_from_json, circuit_to_openqasm
from .optimizer import optimize_circuit
from .var_algo import variational_optimization, vqe_stub, qaoa_stub

# Plugin registry for extensibility.
_plugins = {}

def register_plugin(name: str, func: object) -> None:
    """Register a plugin to extend topoQ functionality."""
    _plugins[name] = func

def get_plugin(name: str) -> object:
    """Retrieve a registered plugin."""
    return _plugins.get(name)

__version__ = "1.0.0"
