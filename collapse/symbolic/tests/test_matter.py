"""Unittests for the Symbolic Matter Module
"""

import pytest

from collapse.symbolic import matter, metric


class TestMatter:
    """Test Matter Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw_metric()

    def test_perfect_fluid_stress_energy(self, met):
        """Test T_mn"""
        expr = matter.perfect_fluid_stress_energy(met).doit()
        assert repr(expr) == ('Matrix([\n'
                              '[p + rho - p/c**2,      0,      0,      0],\n'
                              '[               0, p/a(t),      0,      0],\n'
                              '[               0,      0, p/a(t),      0],\n'
                              '[               0,      0,      0, p/a(t)]])')
