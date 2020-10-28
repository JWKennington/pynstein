"""Unittests for collapse.symbolic.constants module"""

from sympy import symbols
from sympy.diffgeom import CoordSystem as _CoordSystem, Manifold, Patch

from collapse.symbolic import coords
from collapse.symbolic.utilities import tensor_pow as tpow


class TestCoords:

    def test__coord_system_symbols(self):
        manifold = Manifold('M', 4)
        origin_patch = Patch('o', manifold)
        sym_cs = _CoordSystem('cartesian', origin_patch, ['x', 'y', 'z'])
        sym_cs_symbols = coords._coord_system_symbols(sym_cs)
        assert sym_cs_symbols == symbols('x y z')

    def test_toroidal_coords(self):
        cs = coords.toroidal_coords()
        assert len(cs.base_symbols()) == 4  # 4 dim space
        assert str(cs) == "CoordSystem(toroidal, Patch(o, Manifold(M, 4)), (t, r, theta, phi))"

        cs = coords.toroidal_coords(dim=2)
        assert len(cs.base_symbols()) == 2  # 4 dim space
        assert str(cs) == "CoordSystem(toroidal, Patch(o, Manifold(M, 2)), (t, r))"

    def test_cartesian_coords(self):
        cs = coords.cartesian_coords()
        assert len(cs.base_symbols()) == 4  # 4 dim space
        assert str(cs) == "CoordSystem(cartesian, Patch(o, Manifold(M, 4)), (t, x, y, z))"

        cs = coords.cartesian_coords(dim=2)
        assert len(cs.base_symbols()) == 2  # 4 dim space
        assert str(cs) == "CoordSystem(cartesian, Patch(o, Manifold(M, 2)), (t, x))"


class TestCoordSystem:

    def _dummy_cs(self):
        manifold = Manifold('M', 3)
        origin_patch = Patch('o', manifold)
        return coords.CoordSystem('euclidean', origin_patch, ['x', 'y', 'z'])

    def test_create(self):
        cs = self._dummy_cs()
        assert isinstance(cs, coords.CoordSystem)

    def test_base_symbols(self):
        cs = self._dummy_cs()
        coord_syms = cs.base_symbols()
        assert str(coord_syms) == "(x, y, z)"

    def test_from_sympy_coordsystem(self):
        manifold = Manifold('M', 4)
        origin_patch = Patch('o', manifold)
        sym_cs = _CoordSystem('cartesian', origin_patch, ['x', 'y', 'z'])
        cs = coords.CoordSystem.from_sympy_coordsystem(sym_cs)
        assert isinstance(cs, coords.CoordSystem)

    def test_from_twoform(self):
        cs = coords.toroidal_coords(dim=2)
        dt, dr = cs.base_oneforms()
        a, b = symbols('a b')
        form = a * tpow(dt, 2) + b * tpow(dr, 2)
        cs_p = coords.CoordSystem.from_twoform(form)
        assert cs == cs_p
