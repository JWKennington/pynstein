"""Unittests for collapse.symbolic.constants module"""
# pylint: disable=protected-access

from collapse.symbolic import symbols


class TestSymbols:
    """Test Symbols"""

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
