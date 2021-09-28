"""Unittests for the Symbolic Matter Module
"""

import pytest

from pystein import matter, metric


class TestMatter:
    """Test Matter Module"""

    @pytest.fixture(scope='class', autouse=True)
    def met(self):
        """Make metric for other tests"""
        return metric.flrw(cartesian=True)

    def test_vacuum(self, met):
        """Test T_mn"""
        expr = matter.vacuum(met).doit()
        assert repr(expr) == 'Matrix([\n[0, 0, 0, 0],\n[0, 0, 0, 0],\n[0, 0, 0, 0],\n[0, 0, 0, 0]])'

    def test_perfect_fluid(self, met):
        """Test T_mn"""
        expr = matter.perfect_fluid(met).doit()
        assert repr(expr) == ('Matrix([\n'
                              '[\\rho,         0,         0,         0],\n'
                              '[   0, p*a(t)**2,         0,         0],\n'
                              '[   0,         0, p*a(t)**2,         0],\n'
                              '[   0,         0,         0, p*a(t)**2]])')
