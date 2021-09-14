"""Symbolic Coordinates for cosmological calculations

This module extends the analogous module in sympy and adds some new principal
features to the CoordSystem interface. Notably, sympy CoordSystem depends on a
Metric, whereas we've reversed that dependency here. Also, we have made the
underlying coordinates more accessible, instead of relying on coordinate-function
intermediaries.

There is a bug in sympy curvature calculation that makes the
symbols insufficient indices for partial derivatives, which is wrong. As a work
around, sympy forces users to use the coordinate functions as coordinates, which
is mathematically valid but symbolically unfortunate. We emphasize that the
underlying symbols in a coordinate system should be sufficient for differentiation.
"""

from typing import Tuple

from sympy import Symbol, Expr
from sympy.diffgeom import CoordSystem as _CoordSystem, Manifold, Patch

from pystein import symbols

CARTESIAN_SPATIAL_SYMBOLS = [
    symbols.CoordinateSymbol.CartesianX,
    symbols.CoordinateSymbol.CartesianY,
    symbols.CoordinateSymbol.CartesianZ,
]
CARTESIAN_SYMBOLS = [symbols.CoordinateSymbol.Time] + CARTESIAN_SPATIAL_SYMBOLS

SPHERICAL_SPATIAL_SYMBOLS = [
    symbols.CoordinateSymbol.SphericalRadius,
    symbols.CoordinateSymbol.SphericalPolarAngle,
    symbols.CoordinateSymbol.SphericalAzimuthalAngle,
]
SPHERICAL_SYMBOLS = [symbols.CoordinateSymbol.Time] + SPHERICAL_SPATIAL_SYMBOLS


def _coord_system_symbols(coord_system: _CoordSystem) -> Tuple[Symbol, ...]:
    """Small utility function for extracting the underlying symbols from a sympy CoordSystem

    Args:
        coord_system:
            sympy.CoordSystem, the coordsystem from which to extract coordinate symbols

    Returns:
        Tuple[Symbol,...] a tuple of symbols representing the ordered coordinates of the system
    """
    args = coord_system.args
    return args[2]


class CoordSystem(_CoordSystem):
    """Coordinate System class extension of the sympy.diffgeom.CoordSystem class

    This class has the principle difference of being able to produce the base symbols
    used in the coordinates, via the new method 'base_symbols'
    """

    def __new__(cls, name, patch, names=None):
        obj = _CoordSystem.__new__(cls, name, patch, names)
        obj._base_symbols = _coord_system_symbols(obj)
        return obj

    def base_symbols(self):
        """Return the symbols used in the coordinate system"""
        return self._base_symbols

    @staticmethod
    def from_sympy_coordsystem(coord_system: _CoordSystem):
        """Create a CoordSystem from a sympy.diffgeom.CoordSystem"""
        return CoordSystem(name=coord_system.args[0],
                           patch=coord_system.args[1],
                           names=coord_system.args[2])  # pylint: disable=protected-access

    @staticmethod
    def from_twoform(twoform: Expr):
        """Create a CoordSystem from a sympy.Expr that represents a metric as a twoform
        by extracting the coordinates from the given metric (reversing this dependency)
        """
        cs = twoform.atoms(_CoordSystem).pop()
        return CoordSystem.from_sympy_coordsystem(cs)


def toroidal_coords(manifold: Manifold = None, dim: int = 4):
    """Create a Toroidal Coordinate system (t ~ R and (x,y,z) ~ S^3) with maximal
    dimension 4 (can create subspaces too)

    Args:
        manifold:
            Manifold, default None. If specified use this Manifold to take a coordinate patch
        dim:
            int, the dimension of the resulting coordinate system. Must be less than or equal to 4,
                and must match the dimension of the given Manifold if specified.

    Returns:
        CoordSystem, the coordinate system
    """
    if manifold is None:
        manifold = Manifold('M', dim)
    origin_patch = Patch('o', manifold)
    return CoordSystem('toroidal', origin_patch, SPHERICAL_SYMBOLS[:dim])


def cartesian_coords(manifold: Manifold = None, dim: int = 4):
    """Create a Cartesian Coordinate system (t ~ R and (x,y,z) ~ R^3) with maximal
    dimension 4 (can create subspaces too)

    Args:
        manifold:
            Manifold, default None. If specified use this Manifold to take a coordinate patch
        dim:
            int, the dimension of the resulting coordinate system. Must be less than or equal to 4,
                and must match the dimension of the given Manifold if specified.

    Returns:
        CoordSystem, the coordinate system
    """
    if manifold is None:
        manifold = Manifold('M', dim)
    origin_patch = Patch('o', manifold)
    return CoordSystem('cartesian', origin_patch, CARTESIAN_SYMBOLS[:dim])
