"""
Visualization tools for topoQ.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Optional
from .transpiler import circuit_to_json


def draw_circuit(circuit: object, save_path: Optional[str] = None) -> None:
    """
    Draws a static circuit diagram with pleasing colors.
    """
    num_qubits: int = len(circuit.qubits)
    num_ops: int = len(circuit.operations)

    fig, ax = plt.subplots(figsize=(max(8, num_ops * 0.8), num_qubits * 1))
    ax.set_xlim(0, num_ops + 1)
    ax.set_ylim(-0.5, num_qubits - 0.5)
    ax.set_yticks(range(num_qubits))
    ax.set_yticklabels([f"Qubit {i}" for i in range(num_qubits)])
    ax.set_xlabel("Circuit Depth")
    ax.set_title("topoQ Circuit Diagram")

    for i in range(num_qubits):
        ax.hlines(i, 0, num_ops + 1, color="gray", linestyle="--", linewidth=1)

    for op_index, op in enumerate(circuit.operations, start=1):
        op_type = op[0]
        if op_type == "gate":
            gate = op[2]
            gate_name = str(gate).split("(")[0]
            ax.text(op_index, op[1], gate_name, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="skyblue",
                              ec="black", lw=1))
        elif op_type == "measure":
            ax.text(op_index, op[1], f"M({op[2]})", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen",
                              ec="black", lw=1))
        elif op_type == "reset":
            ax.text(op_index, op[1], "RESET", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="lightcoral",
                              ec="black", lw=1))
        elif op_type == "multi_gate":
            indices = op[1]
            ax.text(op_index, min(indices), "MultiGate", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="plum",
                              ec="black", lw=1))

    gate_patch = mpatches.Patch(color="skyblue", label="Gate")
    measure_patch = mpatches.Patch(color="lightgreen", label="Measure")
    reset_patch = mpatches.Patch(color="lightcoral", label="Reset")
    multi_patch = mpatches.Patch(color="plum", label="Multi-Qubit Gate")
    ax.legend(handles=[gate_patch, measure_patch, reset_patch, multi_patch],
              loc="upper right")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def draw_bloch_sphere(qubit: object) -> None:
    """
    Draws a Bloch sphere representation for a single qubit state.
    """
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    a, b = qubit.state
    theta = 2 * np.arccos(np.clip(np.abs(a), 0, 1))
    phi = np.angle(b) - np.angle(a)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    u, v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:25j]
    xs = np.cos(u) * np.sin(v)
    ys = np.sin(u) * np.sin(v)
    zs = np.cos(v)
    ax.plot_surface(xs, ys, zs, color="lightgray", alpha=0.3, edgecolor="none")
    ax.scatter([x], [y], [z], color="red", s=100)
    ax.set_title("Bloch Sphere")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    plt.show()


def interactive_circuit_view(circuit: object) -> None:
    """
    Stub for an interactive circuit viewer.
    For full interactivity, integrate Plotly or Bokeh.
    """
    print("Interactive circuit view (JSON):")
    print(circuit_to_json(circuit))
