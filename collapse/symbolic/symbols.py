"""Module for commonly used symbols, such as coordinate symbols. This prevents unnecessary
duplicate calls to sympy.symbols and provides unified access to reoccurring symbols.
"""

from sympy import Symbol as _Symbol


class CoordinateSymbol:
    """An enumeration of commonly used coordinate symbols"""
    Time = _Symbol('t')
    CartesianX = _Symbol('x')
    CartesianY = _Symbol('y')
    CartesianZ = _Symbol('z')
    SphericalRadius = _Symbol('r')
    SphericalPolarAngle = _Symbol(r'\theta')
    SphericalAzimuthalAngle = _Symbol(r'\varphi')


class CurvatureSymbol:
    """An Enumeration of commonly used curvature symbols"""
    ConstantCurvature = _Symbol('k')


# The below are shorthands for the above commonly used symbols
t = CoordinateSymbol.Time

x = CoordinateSymbol.CartesianX
y = CoordinateSymbol.CartesianY
z = CoordinateSymbol.CartesianZ

r = CoordinateSymbol.SphericalRadius
theta = CoordinateSymbol.SphericalPolarAngle
phi = CoordinateSymbol.SphericalAzimuthalAngle

k = CurvatureSymbol.ConstantCurvature
