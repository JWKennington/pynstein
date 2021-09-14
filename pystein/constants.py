"""Useful Physical Constants

Since the Astropy library provides a wonderful list of predefined constants, the approach
here is to extend those objects to behave like sympy symbols. This prevents duplicate
definitions of physical constants while providing a natural handle for each value when
constructing a symbolic expression using sympy.

We have also extended the Units definition to include natural (Planck) units in which
the physical constants c = G = hbar = kB = 1. These units are a geometrized system ideal
for general relativity (the focus of this package).


References:
    [1] NIST CODATA2018 Value of Planck Length https://physics.nist.gov/cgi-bin/cuu/Value?plkl
    [2] NIST CODATA2018 Value of Planck Mass https://physics.nist.gov/cgi-bin/cuu/Value?plkm
    [3] NIST CODATA2018 Value of Planck Time https://physics.nist.gov/cgi-bin/cuu/Value?plkt
    [4] NIST CODATA2018 Value of Planck Temperatur https://physics.nist.gov/cgi-bin/cuu/Value?plktmp
"""
import enum
import math

from astropy import constants
from astropy.units import Unit, meter, second, Kelvin, kilogram, add_enabled_units, Quantity
from sympy import Symbol, Expr

NATURAL_VALUE = 1


@enum.unique
class UnitSystem(str, enum.Enum):
    """Unit Systems Constants"""
    SI = 'si'
    CGS = 'cgs'
    NATURAL = 'natural'


# DEFINE NATURAL PLANK UNITS
l_P = plank_length = Unit(['l_P', 'Planck_length'], represents=math.sqrt((constants.hbar * constants.G / (constants.c ** 3)).si.value) * meter)
m_P = plank_mass = Unit(['m_P', 'Planck_mass'], represents=math.sqrt((constants.hbar * constants.c / constants.G).si.value) * kilogram)
t_P = plank_time = Unit(['t_P', 'Planck_time'], represents=math.sqrt((constants.hbar * constants.G / (constants.c ** 5)).si.value) * second)
T_P = plank_temp = Unit(['T_P', 'Planck_temp'], represents=math.sqrt((constants.hbar * (constants.c ** 5) / (constants.G * constants.k_B ** 2)).si.value) * Kelvin)

NATURAL_EQUIVALENCIES = [  # TODO make this work with full conversion to natural units
    (meter, l_P, lambda x: l_P.si.scale * x, lambda x: x / l_P.si.scale),
    (second, t_P, lambda x: t_P.si.scale * x, lambda x: x / t_P.si.scale),
    (kilogram, m_P, lambda x: m_P.si.scale * x, lambda x: x / m_P.si.scale),
    (Kelvin, T_P, lambda x: T_P.si.scale * x, lambda x: x / T_P.si.scale),
]

add_enabled_units([l_P, m_P, t_P, T_P])


class ConstantSymbol(Symbol):
    """Constant Symbol is a symbolic representation of a known physical constant,
    as defined in the astropy.constants module.
    """

    def __new__(cls, constant: constants.Constant, is_natural_unit: bool = False):
        s = Symbol.__new__(cls, name=constant.abbrev)
        s._constant = constant
        s._is_natural_unit = is_natural_unit
        return s

    @property
    def cgs(self):
        """Pass-thru accessor to constant value in CGS units"""
        return self.constant.cgs

    @property
    def constant(self):
        """Safe attr access for _constant"""
        return self._constant

    @property
    def is_natural_unit(self):
        """Safe attr access for _is_natural_unit"""
        return self._is_natural_unit

    @property
    def natural(self):
        """Pass-thru accessor to constant value in Natural units"""
        if self._is_natural_unit:
            return Quantity(NATURAL_VALUE, dtype=int)
        raise NotImplementedError('Natural units conversion not yet supported')

    @property
    def si(self):
        """Pass-thru accessor to constant value in SI units"""
        return self.constant.si

    @property
    def unit(self):
        """Safe attr access for constant.unit"""
        return self.constant.unit

    def is_constant(self):
        """Override this method to instantly return True"""
        return True


# Define commonly used constants
c = ConstantSymbol(constants.c, is_natural_unit=True)
G = ConstantSymbol(constants.G, is_natural_unit=True)
h = ConstantSymbol(constants.h)
hbar = ConstantSymbol(constants.hbar, is_natural_unit=True)
k_B = ConstantSymbol(constants.k_B, is_natural_unit=True)


def _subs_const_values(expr: Expr, unit_system: UnitSystem = UnitSystem.SI) -> Expr:
    """Substitute any ConstantSymbols in an Expression with their value in a particular
    system of units

    Args:
        expr:
            Expr, the sympy expression in which to substitute constant symbols for values
        unit_system:
            UnitType, default SI. The system of units in which to evaluate constants

    Returns:
        Expr, the substituted expression
    """
    # Ensure unit_system is UnitType
    if not isinstance(unit_system, UnitSystem):
        unit_system = UnitSystem(unit_system)

    # Determine the free symbols that are ConstantSymbols
    const_syms = tuple(sorted({s for s in expr.free_symbols if isinstance(s, ConstantSymbol)}, key=lambda s: s.name))

    # Check if using Natural units that all are natural unit capable
    if unit_system == UnitSystem.NATURAL and not all(s.is_natural_unit for s in const_syms):
        raise ValueError('Cannot substitute natural units for the following ConstantSymbols: {}'.format(', '.join([str(s) for s in const_syms if not s.is_natural_unit])))

    # Build substitution dictionary
    sub_rules = [(s, getattr(s, unit_system.value).value) for s in const_syms]

    # Perform substitution and return
    return expr.subs(sub_rules)


def subs_si(expr: Expr) -> Expr:
    """Substitute any ConstantSymbols in an Expression with their value in a SI units

    Args:
        expr:
            Expr, the sympy expression in which to substitute constant symbols for values

    Returns:
        Expr, the substituted expression
    """
    return _subs_const_values(expr, unit_system=UnitSystem.SI)


def subs_cgs(expr: Expr) -> Expr:
    """Substitute any ConstantSymbols in an Expression with their value in a CGS units

    Args:
        expr:
            Expr, the sympy expression in which to substitute constant symbols for values

    Returns:
        Expr, the substituted expression
    """
    return _subs_const_values(expr, unit_system=UnitSystem.CGS)


def subs_natural(expr: Expr) -> Expr:
    """Substitute any ConstantSymbols in an Expression with their value in a NATURAL units

    Args:
        expr:
            Expr, the sympy expression in which to substitute constant symbols for values

    Returns:
        Expr, the substituted expression
    """
    return _subs_const_values(expr, unit_system=UnitSystem.NATURAL)
