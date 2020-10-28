"""Unittests for the Symbolic Curvature Module
"""
import pytest

from collapse.symbolic import curvature, metric


class TestCurvature:
    """Test Curvature Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw_metric()

    def test_christoffel_symbol_component(self, met):
        """Test G_mn^l"""
        expr = curvature.christoffel_symbol_component(0, 1, 1, met).doit()
        assert repr(expr) == "Derivative(a(t), t)/(2*c**2)"

    def test_riemann_tensor_component(self, met):
        """Test R_s^r_mn"""
        expr = curvature.riemann_tensor_component(0, 1, 0, 1, met).doit()
        assert repr(expr) == "Derivative(a(t), (t, 2))/(2*c**2) - Derivative(a(t), t)**2/(4*c**2*a(t))"

    def test_ricci_tensor_component(self, met):
        """Test R_mn"""
        expr = curvature.ricci_tensor_component(0, 0, met).doit()
        assert repr(expr) == "-3*Derivative(a(t), (t, 2))/(2*a(t)) + 3*Derivative(a(t), t)**2/(4*a(t)**2)"

    def test_ricci_scalar(self, met):
        """Test R"""
        expr = curvature.ricci_scalar(met).doit()
        assert repr(expr) == ('-3*Derivative(a(t), (t, 2))/(2*a(t)) + 3*Derivative(a(t), t)**2/(4*a(t)**2) '
                              '+ 3*Derivative(a(t), (t, 2))/(2*c**2) + 3*Derivative(a(t), '
                              't)**2/(4*c**2*a(t))')

    def test_einstein_tensor_component(self, met):
        """Test G_mn"""
        expr = curvature.einstein_tensor_component(0, 0, met).doit()
        assert repr(expr) == ('c**2/2 - 3*Derivative(a(t), (t, 2))/(2*a(t)) + 3*Derivative(a(t), '
                              't)**2/(4*a(t)**2)')
