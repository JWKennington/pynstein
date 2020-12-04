"""Module for commonly used symbols, such as coordinate symbols. This prevents unnecessary
duplicate calls to sympy.symbols and provides unified access to reoccurring symbols.
"""

from sympy import Symbol as _Symbol

DEFAULT_NUMERIC_ASSUMPTIONS = {
    # These assumptions are now the default in several places in sympy.diffgeom
    # Abiding them here helps equality criteria
    'real': True,
    'extended_real': True,
    'imaginary': False,
    'commutative': True,
    'infinite': False,
    'complex': True,
    'hermitian': True,
    'finite': True
}


def numeric_symbol(name: str, assumptions: dict = None):
    """Helper utility for creating a numeric symbol with default
    assumptions from the sympy.diffgeom subpackage

    Args:
        name:
            str, the name
        assumptions:
            dict, the assumptions. If None use DEFAULT_NUMERIC_ASSUMPTIONS

    Returns:
        Symbol
    """
    if assumptions is None:
        assumptions = DEFAULT_NUMERIC_ASSUMPTIONS
    return _Symbol(name, **assumptions)


class CoordinateSymbol: # pylint: disable=too-few-public-methods
    """An enumeration of commonly used coordinate symbols"""
    Time = numeric_symbol('t')
    CartesianX = numeric_symbol('x')
    CartesianY = numeric_symbol('y')
    CartesianZ = numeric_symbol('z')
    SphericalRadius = numeric_symbol('r')
    SphericalPolarAngle = numeric_symbol(r'\theta')
    SphericalAzimuthalAngle = numeric_symbol(r'\varphi')


class CurvatureSymbol: # pylint: disable=too-few-public-methods
    """An Enumeration of commonly used curvature symbols"""
    ConstantCurvature = numeric_symbol('k')


class MatterSymbol: # pylint: disable=too-few-public-methods
    """An Enumeration of commonly used matter symbols"""
    Density = numeric_symbol(r'\rho')
    Pressure = numeric_symbol('p')


# The below are shorthands for the above commonly used symbols
t = CoordinateSymbol.Time

x = CoordinateSymbol.CartesianX
y = CoordinateSymbol.CartesianY
z = CoordinateSymbol.CartesianZ

r = CoordinateSymbol.SphericalRadius
theta = CoordinateSymbol.SphericalPolarAngle
phi = CoordinateSymbol.SphericalAzimuthalAngle

k = CurvatureSymbol.ConstantCurvature

rho = MatterSymbol.Density
p = MatterSymbol.Pressure
