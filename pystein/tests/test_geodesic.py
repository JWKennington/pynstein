import numpy
import sympy
from sympy.diffgeom import Manifold, Patch

from pystein import geodesic, metric, coords
from pystein.utilities import tensor_pow as tpow


class TestGeodesic:

	def test_numerical(self):
		M = Manifold('M', dim=2)
		P = Patch('origin', M)

		rho, phi, a = sympy.symbols('rho phi a', nonnegative=True)

		cs = coords.CoordSystem('schw', P, [rho, phi])
		drho, dphi = cs.base_oneforms()
		ds2 = a ** 2 * ((1 / (1 - rho ** 2)) * tpow(drho, 2) + rho ** 2 * tpow(dphi, 2))
		g = metric.Metric(twoform=ds2)
		init = (0.01, 0.01, 0.000001, 0.1)
		ts = numpy.arange(0, 1000, 0.1)
		df = geodesic.numerical_geodesic(g, init, ts)
		print('yay')

	def test_parallel(self):
		M = Manifold('M', dim=2)
		P = Patch('origin', M)

		theta, phi, a = sympy.symbols('theta phi a', nonnegative=True)
		cs = coords.CoordSystem('spherical', P, [theta, phi])
		dtheta, dphi = cs.base_oneforms()
		ds2 = a ** 2 * (tpow(dtheta, 2) + sympy.sin(theta) ** 2 * tpow(dphi, 2))
		g2 = metric.Metric(twoform=ds2)

		param = sympy.symbols('lambda')

		curve = [
			2 * sympy.pi * param,
			sympy.pi / 4,
		]

		lhs_0 = geodesic.parallel_transport_equation(0, curve, param, g2)
		print(lhs_0)
