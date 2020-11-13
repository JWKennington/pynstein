"""Unittests for the Symbolic Gravity Module
"""

import pytest

from collapse.symbolic import gravity, metric, matter


class TestGravity:
    """Test Gravity Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw_metric()

    def test_einstein_equation(self, met):
        """Test G_mn = T_mn"""
        se = matter.perfect_fluid(met)
        expr = gravity.einstein_equation(0, 0, met, stress_energy=se).doit()
        assert repr(expr) == ('Eq(c**2/2 - 3*Derivative(a(t), (t, 2))/(2*a(t)) + 3*Derivative(a(t), '
                              't)**2/(4*a(t)**2), 8*G*pi*(-c**2*p + p + rho)/c**4)')
