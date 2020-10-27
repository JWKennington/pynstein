"""Utilities for constructing symbolic matter expressions, usually via
the Stress-Energy Tensor

"""

from sympy import Array, symbols
from sympy.matrices import diag

from collapse.symbolic.metric import Metric


def perfect_fluid_stress_energy(metric: Metric) -> Array:
    p, rho = symbols('p rho')
    return (p + rho) * diag(1, 0, 0, 0) + p * metric.inverse.matrix
