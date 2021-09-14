"""Symbolic expressions related to gravitation

This module largely serves as a convenience wrapper around the matter and curvature modules,
in that it equates those quantities for fixed components.
"""
import sympy.core.numbers
from sympy import Equality, Expr, pi, Matrix

from pystein import curvature, matter
from pystein import constants
from pystein.metric import Metric

sympy.core.numbers.NegativeOne


def einstein_equation(mu: int, nu: int, metric: Metric, stress_energy: Matrix = None) -> Expr:
    """Compute the einstein equation for coordinates mu and nu. Note that
    this function assumes a perfect fluid for the matter component. In future work
    this component will be modular.

    Args:
        mu:
            int, the lower left index of the Einstein and Stress-Energy Tensors
        nu:
            int, the lower right index of the Einstein and Stress-Energy Tensors
        metric:
            Metric

    Returns:
        Expr, the Einstein field equation for specific coordinates mu and nu
    """
    if stress_energy is None:
        stress_energy = matter.vacuum(metric)
    G_mu_nu = curvature.einstein_tensor_component(mu, nu, metric)
    T_mu_nu = stress_energy[mu, nu]
    return Equality(G_mu_nu, (8 * pi * constants.G / constants.c ** 4) * T_mu_nu)
