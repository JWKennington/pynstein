"""Unittests for pystein.symbolic.constants module"""
# pylint: disable=protected-access
import pytest
from astropy import constants as astro_constants
from sympy import symbols

from pystein import constants
from pystein.constants import UnitSystem


class TestNaturalUnits:
    """Test Natural Units"""

    # TODO this part is in progress
    def test_values(self):
        """Test values"""
        assert str(constants.l_P.represents) == "1.61626e-35 m"
        assert str(constants.m_P.represents) == "2.17643e-08 kg"
        assert str(constants.t_P.represents) == "5.39125e-44 s"
        assert str(constants.T_P.represents) == "1.41678e+32 K"

    def test_equivalencies(self):
        """Test Equivalencies"""
        assert len(constants.NATURAL_EQUIVALENCIES) == 4


class TestUnitSystem:
    """Test UnitSystem enum"""

    def test_values(self):
        """Test Values"""
        assert UnitSystem.SI == 'si'
        assert UnitSystem.CGS == 'cgs'
        assert UnitSystem.NATURAL == 'natural'

        assert UnitSystem.SI.value == 'si'
        assert UnitSystem.SI.name == 'SI'

    def test_value_lookup(self):
        """Test Value Lookup"""
        assert isinstance(UnitSystem('si'), UnitSystem)
        assert UnitSystem('si') == UnitSystem.SI


class TestConstants:
    """Test Constants Module"""

    def test_create(self):
        """Test Create ConstantSymbol"""
        _ = constants.ConstantSymbol(astro_constants.e)
        _ = constants.ConstantSymbol(astro_constants.e, is_natural_unit=True)

    def test_constant_symbol_cgs(self):
        """Test class attrs - cgs"""
        c = constants.c
        assert repr(c.cgs) == "<Quantity 2.99792458e+10 cm / s>"

    def test_constant_symbol_constant(self):
        """Test class attrs - constant"""
        c = constants.c
        assert c.constant == astro_constants.c

    def test_constant_symbol_is_natural_unit(self):
        """Test class attrs - is natural unit"""
        c = constants.c
        assert c.is_natural_unit

    def test_constant_symbol_natural(self):
        """Test class attrs - natural"""
        c = constants.c
        assert repr(c.natural) == "<Quantity 1>"

        with pytest.raises(NotImplementedError):
            _ = constants.h.natural

    def test_constant_symbol_si(self):
        """Test class attrs - si"""
        c = constants.c
        assert c.si == astro_constants.c.si

    def test_constant_symbol_unit(self):
        """Test class attrs - unit"""
        c = constants.c
        assert repr(c.unit) == 'Unit("m / s")'

    def test_constant_symbol_is_constant(self):
        """Test class attrs - constant"""
        c = constants.c
        assert c.is_constant()

    def test_predefined_constants(self):
        """Test Predefined Constants"""
        assert isinstance(constants.c, constants.ConstantSymbol)
        assert isinstance(constants.G, constants.ConstantSymbol)
        assert isinstance(constants.h, constants.ConstantSymbol)
        assert isinstance(constants.hbar, constants.ConstantSymbol)
        assert isinstance(constants.k_B, constants.ConstantSymbol)


class TestConstantSubs:
    """Tests constants substitution"""

    def _dummy_expr(self):
        """Create a dummy expression"""
        x, y = symbols('x y')
        return 2 * constants.c * x + 3 * y / constants.G

    def test__subs_const_values(self):
        """Test helper function for sub"""
        expr = self._dummy_expr()
        subd = constants._subs_const_values(expr, UnitSystem.SI)
        assert repr(subd) == "599584916.0*x + 44948533928.6517*y"

        subd = constants._subs_const_values(expr, 'si')
        assert repr(subd) == "599584916.0*x + 44948533928.6517*y"

    def test_subs_si(self):
        """Test substitute SI values"""
        expr = self._dummy_expr()
        subd = constants.subs_si(expr)
        assert repr(subd) == "599584916.0*x + 44948533928.6517*y"

    def test_subs_cgs(self):
        """Test substitute CGS values"""
        expr = self._dummy_expr()
        subd = constants.subs_cgs(expr)
        assert repr(subd) == "59958491600.0*x + 44948533.9286517*y"

    def test_subs_natural(self):
        """Test substitute NATURAL values"""
        a, b = symbols('a b')
        expr = 4 * constants.c * a + 5 * b / constants.G
        subd = constants.subs_natural(expr)
        assert repr(subd) == "4*a + 5*b"

        with pytest.raises(ValueError):
            expr = expr + constants.h
            constants.subs_natural(expr)
