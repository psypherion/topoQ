"""
Measurement routines for topoQ.
"""

from typing import Dict, List, Tuple


def perform_measurement(qubit: object, basis: str = "Z") -> int:
    """
    Wrapper for Tetron.measure.
    Returns the measurement outcome.
    """
    return qubit.measure(basis)


def compute_error_metrics(
    measurements: List[int], ideal_distribution: Dict[int, float]
) -> Tuple[float, float]:
    """
    Compute total variation distance between measured histogram and ideal distribution.
    Returns a tuple (assignment error, bias error).
    """
    measured = {x: measurements.count(x) / len(measurements) for x in set(measurements)}
    err_a = sum(
        abs(measured.get(x, 0) - ideal_distribution.get(x, 0))
        for x in set(list(measured.keys()) + list(ideal_distribution.keys()))
    )
    err_b = 0.0  # Stub for bias error calculation.
    return err_a, err_b
