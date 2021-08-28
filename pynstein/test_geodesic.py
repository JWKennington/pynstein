import numpy
import sympy
from sympy.diffgeom import Manifold, Patch

from pynstein import geodesic, metric, coords
from pynstein.utilities import tensor_pow as tpow


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