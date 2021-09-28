"""Unittests for pystein package

Presently only a dummy test to confirm repo setup and CI integration
"""
# pylint: disable=protected-access
import pytest
from sympy import Function, symbols, Derivative as D, Array

from pystein import metric, coords
from pystein.utilities import tensor_pow as tpow


class TestMetric:
    """Test Metric module"""

    def _dummy_metric(self):
        """Make a dummy metric"""
        cs = coords.toroidal_coords(dim=2)
        dt, dr = cs.base_oneforms()
        a, b = symbols('a b')
        form = a * tpow(dt, 2) + b * tpow(dr, 2)
        return metric.Metric(twoform=form, components=(a, b))

    def test_create_wrong(self):
        """Test Create wrong"""
        with pytest.raises(ValueError):
            metric.Metric()

    def test_create_from_twoform(self):
        """Test creation from a twoform"""
        g = self._dummy_metric()
        assert isinstance(g, metric.Metric)

    def test_create_from_matrix(self):
        """Test creation from a matrix"""
        cs = coords.toroidal_coords(dim=2)
        a, b = symbols('a b')
        matrix = Array([[a, 0], [0, b]])
        with pytest.raises(ValueError):
            metric.Metric(matrix=matrix)
        g = metric.Metric(matrix=matrix, coord_system=cs)
        assert isinstance(g, metric.Metric)

    def test_repr(self):
        """Test string representation"""
        g = self._dummy_metric()
        assert repr(g) == r"a*TensorProduct(dt, dt) + b*TensorProduct(dr, dr)"

    def test_repr_latex(self):
        """Test LaTeX representation"""
        g = self._dummy_metric()
        assert g._repr_latex_() == '$\\displaystyle a \\operatorname{d}t \\otimes \\operatorname{d}t + b \\operatorname{d}r \\otimes \\operatorname{d}r$'

    def test_properties(self):
        """Test properties"""
        g = self._dummy_metric()
        _ = g.twoform
        _ = g.matrix

    def test_inverse(self):
        """Test Inverse"""
        g = self._dummy_metric()

        # First, check cache is empty
        assert g._inverse is None

        # Then check matrix inverse computes
        i = g.inverse
        assert isinstance(i, metric.Metric)
        assert repr(i) == "TensorProduct(dr, dr)/b + TensorProduct(dt, dt)/a"

        # Last, check result cached
        assert g._inverse is not None

    def test_subs(self):
        """Test Subs"""
        g = self._dummy_metric()
        p = g.subs({g.components[0]: 0})
        assert repr(p.twoform) == "b*TensorProduct(dr, dr)"
        assert p.components == g.components[1:]


class TestPredefinedMetrics:
    """Test predefined metrics"""

    def test_minkowski(self):
        """Test Predefined FLRW metric"""
        assert repr(metric.minkowski()) == ('-TensorProduct(dt, dt) + TensorProduct(dx, dx) + TensorProduct(dy, dy) + '
                                            'TensorProduct(dz, dz)')

    def test_gim(self):
        """Test Predefined GIM metric"""
        assert repr(metric.general_inhomogeneous_isotropic()) == ('L(t, r)**2*TensorProduct(M(t, r)*dt + dr, M(t, r)*dt + dr) - N(t, '
                                                                  'r)**2*TensorProduct(dt, dt) + S(t, '
                                                                  'r)**2*(sin(\\theta)**2*TensorProduct(d\\varphi, d\\varphi) + '
                                                                  'TensorProduct(d\\theta, d\\theta))')

    def test_flrw(self):
        """Test Predefined FLRW metric"""
        assert repr(metric.flrw(cartesian=True)) == ('-c**2*TensorProduct(dt, dt) + a(t)**2*(TensorProduct(dx, dx) + '
                                                     'TensorProduct(dy, dy) + TensorProduct(dz, dz))')

        assert repr(metric.flrw()) == ('-c**2*TensorProduct(dt, dt) + '
                                       'a(t)**2*(r**2*(sin(\\theta)**2*TensorProduct(d\\varphi, d\\varphi) + '
                                       'TensorProduct(d\\theta, d\\theta)) + TensorProduct(dr, dr)/(-k*r**2 + 1))')

        assert repr(metric.flrw(curvature_constant=1)) == ('-c**2*TensorProduct(dt, dt) + '
                                                           'a(t)**2*(r**2*(sin(\\theta)**2*TensorProduct(d\\varphi, d\\varphi) + '
                                                           'TensorProduct(d\\theta, d\\theta)) + TensorProduct(dr, dr)/(1 - r**2))')


class TestMetricDerivativeSimplification:
    """Test metric derivative notation"""

    def test__deriv_simplify_rule(self):
        """Consistency test for version numbers"""
        t, r, phi = symbols('t r phi')
        F = Function('F')(t)
        G = Function('G')(t, r)

        assert metric._deriv_simplify_rule(F, phi)[1] == 0
        assert metric._deriv_simplify_rule(F, t)[1].name == "F'"
        assert metric._deriv_simplify_rule(F, (t, t))[1].name == "F''"
        assert metric._deriv_simplify_rule(F, t, use_dots=True)[1].name == r"\dot{F}"
        assert metric._deriv_simplify_rule(F, (t, t), use_dots=True)[1].name == r"\ddot{F}"
        assert metric._deriv_simplify_rule(G, t)[1].name == "G_{t}"
        assert metric._deriv_simplify_rule(G, (t, t))[1].name == "G_{t t}"
        assert metric._deriv_simplify_rule(G, (t, r))[1].name == "G_{t r}"

    def test_simplify_deriv_notation(self):
        """Test simplify deriv notation"""
        cs = coords.cartesian_coords()
        t, x, *_ = cs.base_symbols()
        dt, dx, *_ = cs.base_oneforms()
        F = Function('F')(t)
        G = Function('G')(t, x)

        form = F ** 2 * tpow(dt, 2) + G ** 2 * tpow(dx, 2)
        g = metric.Metric(twoform=form, components=(F, G))

        # Check First-Order Terms
        assert str(metric.simplify_deriv_notation(D(F, t), g, max_order=1)) == "F'(t)"
        assert str(metric.simplify_deriv_notation(D(F, t), g, max_order=1, use_dots=True)) == r"\dot{F}(t)"

        # Check Second-Order Pure Terms
        assert str(metric.simplify_deriv_notation(D(D(F, t), t), g, max_order=2)) == "F''(t)"
        assert str(metric.simplify_deriv_notation(D(D(F, t), t), g, max_order=2, use_dots=True)) == r"\ddot{F}(t)"

        # Check Second-Order Mixed Terms
        assert str(metric.simplify_deriv_notation(D(D(G, t), t), g, max_order=2)) == "G_{t t}(t, x)"
        assert str(metric.simplify_deriv_notation(D(D(G, t), x), g, max_order=2)) == "G_{t x}(t, x)"
