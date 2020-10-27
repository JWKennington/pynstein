"""Symbolic Curvature Utilities
"""

from sympy import Array, Derivative as D, Rational

from collapse.symbolic.metric import Metric


def christoffel_symbol_component(lam: int, mu: int, nu: int, metric: Metric) -> Array:
    M, MI = metric.matrix, metric.inverse.matrix
    coord_symbols = metric.coord_system.base_symbols()
    dim = len(coord_symbols)
    return Rational(1 / 2) * sum([MI[lam, sig] * (D(M[nu, sig], coord_symbols[mu]) +
                                                  D(M[sig, mu], coord_symbols[nu]) -
                                                  D(M[mu, nu], coord_symbols[sig])) for sig in range(dim)])


def riemann_tensor_component(rho: int, sig: int, mu: int, nu: int, metric: Metric):
    G = lambda lam, mu, nu: christoffel_symbol_component(lam, mu, nu, metric)
    coord_symbols = metric.coord_system.base_symbols()
    dim = len(coord_symbols)
    return D(G(rho, nu, sig), coord_symbols[mu]) - D(G(rho, mu, sig), coord_symbols[nu]) + \
           sum([G(rho, mu, lam) * G(lam, nu, sig) for lam in range(dim)]) - \
           sum([G(rho, nu, lam) * G(lam, mu, sig) for lam in range(dim)])


def ricci_tensor_component(mu: int, nu: int, metric: Metric):
    R = lambda r, s, m, n: riemann_tensor_component(r, s, m, n, metric=metric)
    return sum([R(lam, mu, lam, nu) for lam in range(metric.coord_system.dim)])


def ricci_scalar(metric: Metric):
    return sum(ricci_tensor_component(lam, lam) for lam in range(metric.coord_system.dim))


def einstein_tensor_component(mu: int, nu: int, metric: Metric):
    return ricci_tensor_component(mu, nu, metric) - Rational(1, 2) * metric.matrix[mu, nu]
