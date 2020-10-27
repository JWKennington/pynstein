"""Symbolic Coordinates for cosmological calculations
"""

from typing import Tuple

from sympy import Symbol, Expr
from sympy.diffgeom import CoordSystem as _CoordSystem, Manifold, Patch


def _coord_system_symbols(coord_system: _CoordSystem) -> Tuple[Symbol]:
    return coord_system.args[-1]


class CoordSystem(_CoordSystem):
    def __new__(cls, name, patch, names=None):
        obj = _CoordSystem.__new__(cls, name, patch, names)
        obj._base_symbols = _coord_system_symbols(obj)
        return obj

    def base_symbols(self):
        return self._base_symbols

    @staticmethod
    def from_sympy_coordsystem(coord_system: _CoordSystem):
        return CoordSystem(name=coord_system.name,
                           patch=coord_system.patch,
                           names=coord_system._names)

    @staticmethod
    def from_twoform(twoform: Expr):
        cs = twoform.atoms(_CoordSystem).pop()
        return CoordSystem.from_sympy_coordsystem(cs)


def toroidal_coords(manifold: Manifold = None, dim: int = 4):
    if manifold is None:
        manifold = Manifold('M', dim)
    origin_patch = Patch('o', manifold)
    return CoordSystem('toroidal', origin_patch, ['t', 'r', 'theta', 'phi'][:dim])


def cartesian_coords(manifold: Manifold = None):
    if manifold is None:
        manifold = Manifold('M', 4)
    origin_patch = Patch('o', manifold)
    return CoordSystem('cartesian', origin_patch, ['t', 'x', 'y', 'z'])
