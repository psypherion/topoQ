#!/usr/bin/env python
"""
Command-line interface (CLI) for topoQ.
Provides subcommands to build, simulate, and optimize circuits.
"""

import argparse
import sys
from colorama import init, Fore
init(autoreset=True)

from topoQ.qubit import Tetron
from topoQ.circuit import Circuit
from topoQ.gates import BraidingGate, CliffordGate
from topoQ.simulation import Simulation
from topoQ.visualization import draw_circuit
from topoQ.transpiler import circuit_to_json, circuit_to_openqasm
from topoQ.optimizer import optimize_circuit


def build_sample_circuit(theta: float) -> Circuit:
    circuit = Circuit()
    circuit.add_qubit(Tetron())
    braid_gate = BraidingGate(theta=theta, generator="X")
    circuit.apply_gate(braid_gate, qubit_index=0)
    h_gate = CliffordGate("H")
    circuit.apply_gate(h_gate, qubit_index=0)
    circuit.measure(0, basis="Z")
    return circuit


def cmd_build(args: argparse.Namespace) -> None:
    circuit = build_sample_circuit(args.theta)
    print(Fore.CYAN + "Built circuit:")
    print(circuit)
    draw_circuit(circuit)
    if args.export_json:
        json_str = circuit_to_json(circuit)
        print(Fore.GREEN + "Circuit JSON representation:")
        print(json_str)
    if args.export_qasm:
        qasm_str = circuit_to_openqasm(circuit)
        print(Fore.GREEN + "Circuit OpenQASM representation:")
        print(qasm_str)


def cmd_simulate(args: argparse.Namespace) -> None:
    circuit = build_sample_circuit(args.theta)
    sim = Simulation(circuit=circuit)
    print(Fore.CYAN + "Running simulation...")
    results = sim.run(shots=args.shots)
    print(Fore.MAGENTA + "Measurement Histogram:")
    print(results)


def cmd_optimize(args: argparse.Namespace) -> None:
    circuit = build_sample_circuit(args.theta)
    print(Fore.CYAN + "Original circuit:")
    draw_circuit(circuit)
    optimized = optimize_circuit(circuit)
    print(Fore.CYAN + "Optimized circuit:")
    draw_circuit(optimized)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="topoQ CLI: Build, simulate, and optimize topological circuits."
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    parser_build = subparsers.add_parser("build", help="Build and visualize a sample circuit.")
    parser_build.add_argument("--theta", type=float, default=0.785, help="Braiding angle (radians)")
    parser_build.add_argument("--export-json", action="store_true", help="Export circuit to JSON")
    parser_build.add_argument("--export-qasm", action="store_true", help="Export circuit to OpenQASM format")
    parser_build.set_defaults(func=cmd_build)

    parser_sim = subparsers.add_parser("simulate", help="Run simulation on a sample circuit.")
    parser_sim.add_argument("--theta", type=float, default=0.785, help="Braiding angle (radians)")
    parser_sim.add_argument("--shots", type=int, default=1024, help="Number of simulation shots")
    parser_sim.set_defaults(func=cmd_simulate)

    parser_opt = subparsers.add_parser("optimize", help="Optimize a sample circuit.")
    parser_opt.add_argument("--theta", type=float, default=0.785, help="Braiding angle (radians)")
    parser_opt.set_defaults(func=cmd_optimize)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
