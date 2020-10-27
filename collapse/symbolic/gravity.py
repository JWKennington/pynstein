"""Symbolic expressions related to gravitation
"""

from sympy import Equality
from collapse.symbolic import curvature, matter
from collapse.symbolic.metric import Metric


def einstein_equation(mu: int, nu: int, metric: Metric):
    G_mu_nu = curvature.einstein_tensor_component(mu, nu, metric)
    T_mu_nu = matter.perfect_fluid_stress_energy(metric)[mu, nu]
    return Equality(G_mu_nu, T_mu_nu)
