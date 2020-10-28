"""Symbolic expressions related to gravitation

This module largely serves as a convenience wrapper around the matter and curvature modules,
in that it equates those quantities for fixed components.
"""

from sympy import Equality, Expr

from collapse.symbolic import curvature, matter
from collapse.symbolic.metric import Metric


def einstein_equation(mu: int, nu: int, metric: Metric) -> Expr:
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
    G_mu_nu = curvature.einstein_tensor_component(mu, nu, metric)
    T_mu_nu = matter.perfect_fluid_stress_energy(metric)[mu, nu]
    return Equality(G_mu_nu, T_mu_nu)
