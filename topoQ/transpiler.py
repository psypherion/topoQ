"""
Transpiler module: Converts Circuit objects to JSON and OpenQASM.
"""

import json
from datetime import datetime
from typing import Any
from .circuit import Circuit


def circuit_to_json(circuit: Circuit) -> str:
    """
    Converts a Circuit object to a JSON string with metadata.
    """
    ops_list = []
    for op in circuit.operations:
        if op[0] == "gate":
            gate = op[2]
            op_dict = {
                "type": "gate",
                "qubit": op[1],
                "name": str(gate).split("(")[0],
                "timestamp": datetime.utcnow().isoformat()
            }
            if hasattr(gate, "theta"):
                op_dict["theta"] = gate.theta
            if hasattr(gate, "generator_name"):
                op_dict["generator"] = gate.generator_name
            ops_list.append(op_dict)
        elif op[0] == "measure":
            ops_list.append({
                "type": "measure",
                "qubit": op[1],
                "basis": op[2],
                "timestamp": datetime.utcnow().isoformat()
            })
        elif op[0] == "reset":
            ops_list.append({
                "type": "reset",
                "qubit": op[1],
                "timestamp": datetime.utcnow().isoformat()
            })
        elif op[0] == "multi_gate":
            ops_list.append({
                "type": "multi_gate",
                "qubits": op[1],
                "name": str(op[2]).split("(")[0],
                "timestamp": datetime.utcnow().isoformat()
            })
    circuit_dict: dict = {
        "num_qubits": len(circuit.qubits),
        "operations": ops_list,
        "generated_at": datetime.utcnow().isoformat()
    }
    return json.dumps(circuit_dict, indent=2)


def circuit_from_json(json_str: str) -> Circuit:
    """
    Reconstructs a Circuit object from its JSON representation.
    """
    data: dict = json.loads(json_str)
    from .qubit import Tetron
    from .circuit import Circuit
    circ = Circuit()
    num_qubits: int = data.get("num_qubits", 0)
    for _ in range(num_qubits):
        circ.add_qubit(Tetron())
    for op in data["operations"]:
        if op["type"] == "gate":
            name = op["name"]
            if name == "BraidingGate":
                from .gates import BraidingGate
                theta = op.get("theta", 0)
                generator = op.get("generator", "X")
                gate = BraidingGate(theta=theta, generator=generator)
            elif name == "CliffordGate":
                from .gates import CliffordGate
                gate = CliffordGate("H")
            elif name == "TGate":
                from .gates import TGate
                gate = TGate()
            else:
                from .gates import CliffordGate
                gate = CliffordGate("H")
            circ.apply_gate(gate, op["qubit"])
        elif op["type"] == "measure":
            circ.measure(op["qubit"], basis=op["basis"])
        elif op["type"] == "reset":
            circ.reset(op["qubit"])
        elif op["type"] == "multi_gate":
            pass  # Stub: skip multi-qubit gate reconstruction.
    return circ


def circuit_to_openqasm(circuit: Circuit) -> str:
    """
    Stub: Converts a Circuit object to an OpenQASM-like string.
    """
    qasm_lines = ["OPENQASM 3;"]
    num_qubits: int = len(circuit.qubits)
    qasm_lines.append(f"qubit[{num_qubits}] q;")
    for op in circuit.operations:
        if op[0] == "gate":
            qasm_lines.append(f"// {str(op[2])} on q[{op[1]}]")
        elif op[0] == "measure":
            qasm_lines.append(f"measure q[{op[1]}] -> c[{op[1]}];")
        elif op[0] == "reset":
            qasm_lines.append(f"reset q[{op[1]}];")
    return "\n".join(qasm_lines)
