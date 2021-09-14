"""Symbolic Curvature Utilities

This module provides functions for computing components of various curvature-related
tensors, such as Christoffel symbols, Riemann Tensor, and Ricci Tensor. While the
sympy module does offer analogous functions in the sympy.diffgeom subpackage, there is
an obnoxious bug in that derivatives must be take with respect to coordinate functions
as opposed to the identical symbol. We remediate that shortcoming here, allowing for
maximal interoperability with the other sympy utilies for solving differential equations
and computing derivatives.
"""
import itertools

import sympy
from sympy import Derivative as D, Rational, Expr

from pystein import utilities
from pystein.metric import Metric


def christoffel_symbol_component(lam: int, mu: int, nu: int, metric: Metric) -> Expr:
	"""Compute a component of the Chrisoffel symbol for a particular metric corresponding to

		G_mn^l = 1/2 g^ms (p_m g_ns + p_n g_sm - p_s g_mn)

	Args:
		lam:
			int, Upper index of Christoffel symbol
		mu:
			int, lower left index of Christoffel symbol
		nu:
			int, lower right index of Christoffel symbol
		metric:
			Metric

	Returns:
		Expression of the G_mn^l
	"""
	M = metric.matrix
	I = metric.inverse.matrix
	coord_symbols = metric.coord_system.base_symbols()
	dim = len(coord_symbols)
	return Rational(1, 2) * sum([I[lam, sig] * (D(M[nu, sig], coord_symbols[mu]) +
												D(M[sig, mu], coord_symbols[nu]) -
												D(M[mu, nu], coord_symbols[sig])) for sig in range(dim)])


def riemann_tensor_component(rho: int, sig: int, mu: int, nu: int, metric: Metric, simplify_intermediate: bool = False) -> Expr:
	"""Compute a component of the Riemann Tensor for a particular metric corresponding to

		R^r_smn = p_m G_ns^r - p_n G_ms^r + G_ml^r G_ns^l - G_nl^r G_ms^l

	Args:
		rho:
			int, Upper index of the Riemann Tensor
		sig:
			int, lower left index of Riemann Tensor
		mu:
			int, lower middle index of Riemann Tensor
		nu:
			int, lower right index of Riemann Tensor
		metric:
			Metric

	Returns:
		Expression of the R^r_smn
	"""

	def G(l, m, n):
		"""Shorthand"""
		c = christoffel_symbol_component(l, m, n, metric)
		return sympy.simplify(c) if simplify_intermediate else c

	coord_symbols = metric.coord_system.base_symbols()
	dim = len(coord_symbols)
	return D(G(rho, nu, sig), coord_symbols[mu]) - \
		   D(G(rho, mu, sig), coord_symbols[nu]) + \
		   sum([G(rho, mu, lam) * G(lam, nu, sig) for lam in range(dim)]) - \
		   sum([G(rho, nu, lam) * G(lam, mu, sig) for lam in range(dim)])


def ricci_tensor_component(mu: int, nu: int, metric: Metric, simplify_intermediate: bool = False):
	"""Compute a component of the Ricci Tensor for a particular metric corresponding to

		R_mn = R_m^l_ln

	Args:
		mu:
			int, lower left index of Ricci Tensor
		nu:
			int, lower right index of Ricci Tensor
		metric:
			Metric

	Returns:
		Expression of the R_mn
	"""

	def R(r, s, m, n):
		"""Shorthand"""
		r = riemann_tensor_component(r, s, m, n, metric=metric, simplify_intermediate=simplify_intermediate)
		return sympy.simplify(r) if simplify_intermediate else r

	return sum([R(lam, mu, lam, nu) for lam in range(metric.coord_system.dim)])


def ricci_scalar(metric: Metric, simplify_intermediate: bool = False) -> Expr:
	"""Compute the Ricci Scalar for a particular metric corresponding to

		R = R^l_l = g^mn R_mn

	Args:
		metric:
			Metric

	Returns:
		Expression of R
	"""
	I = metric.inverse.matrix
	return sum(sum(I[lam, rho] * ricci_tensor_component(rho, lam, metric=metric, simplify_intermediate=simplify_intermediate) for rho in range(metric.coord_system.dim)) for lam in range(metric.coord_system.dim))


def einstein_tensor_component(mu: int, nu: int, metric: Metric):
	"""Compute a component of the Einstein Tensor for a particular metric corresponding to

		G_mn = R_mn - (1/2) R g_mn

	Args:
		mu:
			int, lower left index of Einstein Tensor
		nu:
			int, lower right index of Einstein Tensor
		metric:
			Metric

	Returns:
		Expression of the G_mn
	"""
	return ricci_tensor_component(mu, nu, metric) - Rational(1, 2) * ricci_scalar(metric) * metric.matrix[mu, nu]


def compute_components(metric: Metric, non_trivial: bool = True):
	N = len(metric.coord_system.base_symbols())
	christoffels = [((m, n, l), utilities.full_simplify(christoffel_symbol_component(l, m, n, metric=metric))) for l, m, n in itertools.product(range(N), range(N), range(N))]
	riemanns = [((m, n, r, s), utilities.full_simplify(riemann_tensor_component(r, s, m, n, metric=metric))) for m, n, r, s in
				itertools.product(range(N), range(N), range(N), range(N))]
	riccis = [((m, n), utilities.full_simplify(ricci_tensor_component(m, n, metric=metric))) for m, n in itertools.product(range(N), range(N))]

	if non_trivial:
		christoffels = [x for x in christoffels if x[1]]
		riemanns = [x for x in riemanns if x[1]]
		riccis = [x for x in riccis if x[1]]

	return christoffels, riemanns, riccis


def display_components(cps):
	label_names = ['\\mu', '\\nu', '\\rho', '\\sigma'][:len(cps)]
	exprs = [c[1] for c in cps]
	labels = [c[0] for c in cps]
	utilities.concat_latex(exprs, labels, label_names, display=True)


