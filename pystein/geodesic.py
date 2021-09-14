"""Utilities for solving geodesic equation

"""
import itertools
import typing
from collections import namedtuple

import numpy
import pandas
import sympy
from scipy import integrate

from pystein import metric, curvature, utilities


class Solution:
	def __init__(self, soln: typing.List[sympy.Eq], vec_funcs: typing.List[sympy.Function], param: sympy.Symbol, curve: typing.List[sympy.Expr],
				 g: metric.Metric, eqns: typing.List[sympy.Eq]):
		self.soln = soln
		self._vec_funcs = vec_funcs
		self._param = param
		self._curve = curve
		self._metric = g
		self.eqns = eqns

	def vec(self, val: sympy.Expr):
		cs = self._metric.coord_system.base_symbols()
		param_sub = {self._param: val}
		subs = [(c, func.subs(param_sub)) for c, func in zip(cs, self._curve)]
		subs += [(self._param, val)]
		return [self.soln[n].args[1].subs(subs) for n in range(len(self.soln))]


def path_coord_func(coord, param):
	return sympy.Function(coord.name)(param)


def vec_coord_func(coord, param):
	return sympy.Function('v^{{{}}}'.format(coord.name))(param)


def parallel_transport_equation(mu: int, curve: typing.List[sympy.Function], param: sympy.Symbol, g: metric.Metric):
	base_symbols = g.coord_system.base_symbols()

	curve_subs = dict(zip(base_symbols, curve))

	N = len(base_symbols)

	vec_coord_func_map = {s: vec_coord_func(s, param) for s in base_symbols}

	v_mu = vec_coord_func_map[base_symbols[mu]]
	lhs = sympy.diff(v_mu, param)

	for sig in range(N):
		x_sig = curve[sig]
		dx_sig_d_param = sympy.diff(x_sig, param)

		for rho in range(N):
			v_rho = vec_coord_func_map[base_symbols[rho]]
			c_sig_rho = curvature.christoffel_symbol_component(mu, sig, rho, metric=g)
			c_sig_rho = c_sig_rho.doit().subs(curve_subs)
			lhs += c_sig_rho * dx_sig_d_param * v_rho

	return lhs


def parallel_transport_soln(param: sympy.Symbol, curve: typing.List[sympy.Expr], g: metric.Metric):
	bs = g.coord_system.base_symbols()

	# Vector
	v0 = sympy.Function('v^{{{}}}'.format(bs[0].name))
	v1 = sympy.Function('v^{{{}}}'.format(bs[1].name))

	lhs_0 = utilities.full_simplify(parallel_transport_equation(0, curve, param, g).doit())
	lhs_1 = utilities.full_simplify(parallel_transport_equation(1, curve, param, g).doit())

	eqns = [
		sympy.Eq(lhs_0, 0),
		sympy.Eq(lhs_1, 0),
	]
	funcs = [v0(param), v1(param)]

	# Initial Conditions
	ics = {v0(0): v0(0), v1(0): v1(0)}

	soln = sympy.dsolve(eqns, funcs, ics=ics)
	return Solution(soln, [v0, v1], param, curve, g, eqns)


def geodesic_equation(mu: int, param, metric: metric.Metric):
	base_symbols = metric.coord_system.base_symbols()

	coord_func_map = {s: path_coord_func(s, param) for s in base_symbols}

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


def numerical_sampler(g: metric.Metric, ls: numpy.ndarray, init_point: tuple, tangent_scale: float = 1, num_angles: int = 12):
	dfs = []
	for theta_0 in numpy.arange(0.0, 2 * numpy.pi, numpy.pi / num_angles):
		_df = numerical_geodesic(g, tuple(list(init_point) + [tangent_scale * numpy.cos(theta_0), tangent_scale * numpy.sin(theta_0)]), ls)
		_df = _df.assign(theta_0=theta_0)
		dfs.append(_df)
	return pandas.concat(dfs, axis=0)
