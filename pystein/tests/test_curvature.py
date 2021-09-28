"""Unittests for the Symbolic Curvature Module
"""
import pytest

from pystein import curvature, metric
from pystein.utilities import clean_expr


class TestCurvature:
    """Test Curvature Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw(cartesian=True)

    def test_christoffel_symbol_component(self, met):
        """Test G_mn^l"""
        expr = curvature.christoffel_symbol_component(0, 1, 1, met).doit()
        assert repr(expr) == 'a(t)*Derivative(a(t), t)/c**2'

    def test_riemann_tensor_component(self, met):
        """Test R_s^r_mn"""
        expr = curvature.riemann_tensor_component(0, 1, 0, 1, met).doit()
        assert repr(expr) == 'a(t)*Derivative(a(t), (t, 2))/c**2'

    def test_ricci_tensor_component(self, met):
        """Test R_mn"""
        expr = curvature.ricci_tensor_component(0, 0, met).doit()
        assert repr(expr) == '-3*Derivative(a(t), (t, 2))/a(t)'

    def test_ricci_scalar(self, met):
        """Test R"""
        expr = curvature.ricci_scalar(met).doit()
        assert repr(clean_expr(expr)) == '6*(a(t)*Derivative(a(t), (t, 2)) + Derivative(a(t), t)**2)/a(t)**2'

    def test_einstein_tensor_component(self, met):
        """Test G_mn"""
        expr = curvature.einstein_tensor_component(0, 0, met).doit()
        assert repr(clean_expr(expr)) == '3*Derivative(a(t), t)**2/a(t)**2'


class TestFLRW:
    """Test FLRW Curvature Components for accuracy"""

    def test_flrw_christoffel_symbols(self):
        """Test FLRW Christoffel Symbols"""
        g = metric.flrw(cartesian=True)
        G_t_xx = curvature.christoffel_symbol_component(0, 1, 1, g)

        assert str(clean_expr(G_t_xx)) == 'a(t)*Derivative(a(t), t)'

    def test_flrw_ricci_cartesian(self):
        """FLRW Ricci Cartesian"""
        g = metric.flrw(cartesian=True)
        R_tt = curvature.ricci_tensor_component(0, 0, g)
        R_xx = curvature.ricci_tensor_component(1, 1, g)
        R_yy = curvature.ricci_tensor_component(2, 2, g)
        R_zz = curvature.ricci_tensor_component(3, 3, g)

        assert str(clean_expr(R_tt)) == '-3*Derivative(a(t), (t, 2))/a(t)'
        assert str(clean_expr(R_xx)) == 'a(t)*Derivative(a(t), (t, 2)) + 2*Derivative(a(t), t)**2'
        assert str(clean_expr(R_yy)) == 'a(t)*Derivative(a(t), (t, 2)) + 2*Derivative(a(t), t)**2'
        assert str(clean_expr(R_zz)) == 'a(t)*Derivative(a(t), (t, 2)) + 2*Derivative(a(t), t)**2'

    def test_flrw_ricci_scalar_cartesian(self):
        """FLRW Ricci Cartesian"""
        g = metric.flrw(cartesian=True)
        R = curvature.ricci_scalar(g)

        assert str(clean_expr(R)) == '6*(a(t)*Derivative(a(t), (t, 2)) + Derivative(a(t), t)**2)/a(t)**2'

    def test_flrw_einstein_cartesian(self):
        """FLRW Einstein"""
        g = metric.flrw(cartesian=True)
        G_tt = curvature.einstein_tensor_component(0, 0, g)

        assert str(clean_expr(G_tt)) == '3*Derivative(a(t), t)**2/a(t)**2'

    def test_flrw_einstein_k(self):
        """FLRW Einstein"""
        g = metric.flrw()
        G_tt = curvature.einstein_tensor_component(0, 0, g)

        assert str(clean_expr(G_tt)) == '3*(k + Derivative(a(t), t)**2)/a(t)**2'
