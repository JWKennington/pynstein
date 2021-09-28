"""Utilities for constructing symbolic matter expressions, usually via the Stress-Energy Tensor
"""

from sympy import Array
from sympy.matrices import diag, zeros

from pystein import symbols
from pystein import constants
from pystein.metric import Metric


def vacuum(metric: Metric) -> Array:
    """Compute the stress energy tensor for a vacuum (zeros)

    Args:
        metric:
            Metric

    Returns:
        Array, the full stress energy tensor as a matrix
    """
    dim = metric.coord_system.dim
    return zeros(dim, dim)


def perfect_fluid(metric: Metric, fluid_velocity: Array = None) -> Array:
    """Compute the stress energy tensor for a perfect fluid in a given metric

    Args:
        metric:
            Metric

    Returns:
        Array, the full stress energy tensor as a matrix
    """
    p, rho = symbols.p, symbols.rho
    dim = metric.coord_system.dim

    if fluid_velocity is None:  # if not specified choose rest frame fluid velocity
        fluid_velocity = diag(*[1, 0, 0, 0][:dim])

    return (p + rho) * fluid_velocity + p * constants.subs_natural(metric.matrix)
