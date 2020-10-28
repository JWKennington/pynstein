"""Unittests for collapse.symbolic.constants module"""
import pytest
from astropy import constants as astro_constants
from sympy import symbols

from collapse.symbolic import constants
from collapse.symbolic.constants import UnitSystem


class TestNaturalUnits:
    # TODO this part is in progress
    def test_values(self):
        assert str(constants.l_P.represents) == "1.61626e-35 m"
        assert str(constants.m_P.represents) == "2.17643e-08 kg"
        assert str(constants.t_P.represents) == "5.39125e-44 s"
        assert str(constants.T_P.represents) == "1.41678e+32 K"

    def test_equivalencies(self):
        assert len(constants.NATURAL_EQUIVALENCIES) == 4


class TestUnitSystem:

    def test_values(self):
        assert UnitSystem.SI == 'si'
        assert UnitSystem.CGS == 'cgs'
        assert UnitSystem.NATURAL == 'natural'

        assert UnitSystem.SI.value == 'si'
        assert UnitSystem.SI.name == 'SI'

    def test_value_lookup(self):
        assert isinstance(UnitSystem('si'), UnitSystem)
        assert UnitSystem('si') == UnitSystem.SI


class TestConstants:

    def test_create(self):
        x = constants.ConstantSymbol(astro_constants.e)
        _ = constants.ConstantSymbol(astro_constants.e, is_natural_unit=True)

    def test_predefined_constants(self):
        assert isinstance(constants.c, constants.ConstantSymbol)
        assert isinstance(constants.G, constants.ConstantSymbol)
        assert isinstance(constants.h, constants.ConstantSymbol)
        assert isinstance(constants.hbar, constants.ConstantSymbol)
        assert isinstance(constants.k_B, constants.ConstantSymbol)


class TestConstantSubs:

    def _dummy_expr(self, include_non_natural: bool = False):
        x, y = symbols('x y')
        expr = 2*constants.c*x + 3*y/constants.G
        return expr + constants.h if include_non_natural else expr

    def test__subs_const_values(self):
        expr = self._dummy_expr()
        subd = constants._subs_const_values(expr, UnitSystem.SI)
        assert repr(subd) == "599584916.0*x + 44948533928.6517*y"

    def test_subs_si(self):
        expr = self._dummy_expr()
        subd = constants.subs_si(expr)
        assert repr(subd) == "599584916.0*x + 44948533928.6517*y"

    def test_subs_cgs(self):
        expr = self._dummy_expr()
        subd = constants.subs_cgs(expr)
        assert repr(subd) == "59958491600.0*x + 44948533.9286517*y"

    def test_subs_natural(self):
        expr = self._dummy_expr()
        subd = constants.subs_natural(expr)
        assert repr(subd) == "2.0*x + 3.0*y"

        with pytest.raises(ValueError):
            constants.subs_natural(self._dummy_expr(include_non_natural=True))
