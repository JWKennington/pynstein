"""Utilities for solving geodesic equation

"""
import itertools

import pandas
import sympy
from scipy import integrate

from pynstein import metric, curvature, utilities


def path_coord_func(coord, param):
	return sympy.Function(coord.name)(param)


def geodesic_equation(mu: int, param, metric: metric.Metric):
	base_symbols =metric.coord_system.base_symbols()

	coord_func_map = {s: path_coord_func(s, param) for s in base_symbols }

	x_mu = coord_func_map[base_symbols[mu]]

	lhs = sympy.diff(sympy.diff(x_mu, param))
	for rho, sig in itertools.product(range(len(base_symbols)), range(len(base_symbols))):
		x_rho = coord_func_map[base_symbols[rho]]
		x_sig = coord_func_map[base_symbols[rho]]
		c = curvature.christoffel_symbol_component(mu, rho, sig, metric=metric).subs(coord_func_map)
		lhs += c * sympy.diff(x_rho, param) * sympy.diff(x_sig, param)
	return lhs


def numerical_geodesic(g: metric.Metric, init, ts):
	coords = g.coord_system.base_symbols()
	N = len(coords)
	param = sympy.symbols('lambda')
	lhss = [utilities.full_simplify(geodesic_equation(mu, param, metric=g)) for mu in range(N)]

	funcs = [sympy.Function(c.name)(param) for c in coords]

	sub_map = [(sympy.diff(sympy.diff(func, param), param), sympy.symbols('{}2'.format(func.name))) for func in funcs] + \
			  [(sympy.diff(func, param), sympy.symbols('{}1'.format(func.name))) for func in funcs] + \
			  [(func, sympy.symbols('{}0'.format(func.name))) for func in funcs]

	coord2_eqns = [sympy.solve(lhs.subs(sub_map), sympy.symbols('{}2'.format(func.name)))[0] for lhs, func in zip(lhss, funcs)]

	state_symbols = list(sympy.symbols(['{}0'.format(c.name) for c in coords])) + list(sympy.symbols(['{}1'.format(c.name) for c in coords]))
	dcoord1s = [sympy.lambdify(state_symbols, eqn) for eqn in coord2_eqns]

	def integrand(state, param):
		return [s for s in state[N:]] + [s(*state) for s in dcoord1s]

	res = integrate.odeint(integrand, init, ts)
	df = pandas.DataFrame(res[:, :N], columns=[c.name for c in coords])
	return df


