"""Unittests for the Symbolic Gravity Module
"""

import pytest

from pystein import gravity, metric, matter
from pystein.utilities import clean_expr


class TestGravity:
    """Test Gravity Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw()

    def test_einstein_equation(self, met):
        """Test G_mn = T_mn"""
        se = matter.perfect_fluid(met)
        expr = gravity.einstein_equation(0, 0, met, stress_energy=se).doit()
        assert repr(clean_expr(expr)) == 'Eq(8*pi*\\rho, 3*(k + Derivative(a(t), t)**2)/a(t)**2)'

        expr = gravity.einstein_equation(0, 0, met, stress_energy=None).doit()
        assert repr(clean_expr(expr)) == 'Eq(3*(k + Derivative(a(t), t)**2)/a(t)**2, 0)'
