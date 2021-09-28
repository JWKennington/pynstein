"""Unittests for pystein.symbolic.constants module"""
# pylint: disable=protected-access

from pystein import symbols


class TestSymbols:
    """Test Symbols"""

    def test_numeric_symbol(self):
        """Test numeric symbol"""
        a = symbols.numeric_symbol('a')
        assert str(a) == 'a'
        assert a._assumptions == symbols.DEFAULT_NUMERIC_ASSUMPTIONS

    def test_coordinate_symbol(self):
        """Test values"""
        assert str(symbols.t) == "t"

        assert str(symbols.x) == "x"
        assert str(symbols.y) == "y"
        assert str(symbols.z) == "z"

        assert str(symbols.r) == "r"
        assert str(symbols.theta) == r"\theta"
        assert str(symbols.phi) == r"\varphi"

    def test_curvature_symbol(self):
        """Test values"""
        assert str(symbols.k) == "k"

    def test_matter_symbol(self):
        """Test values"""
        assert str(symbols.rho) == r'\rho'
        assert str(symbols.p) == 'p'
