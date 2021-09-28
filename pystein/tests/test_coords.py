"""Unittests for pystein.symbolic.constants module"""
# pylint: disable=protected-access
from sympy import symbols
from sympy.diffgeom import CoordSystem as _CoordSystem, Manifold, Patch

from pystein import coords
from pystein.utilities import tensor_pow as tpow


class TestCoords:
    """Test Coords Module"""

    def test__coord_system_symbols(self):
        """Test coord symbol extraction"""
        manifold = Manifold('M', 4)
        origin_patch = Patch('o', manifold)
        x, y, z = symbols('x y z')
        sym_cs = _CoordSystem('cartesian', origin_patch, [x, y, z])
        sym_cs_symbols = coords._coord_system_symbols(sym_cs)
        assert sym_cs_symbols == symbols('x y z')

    def test_toroidal_coords(self):
        """Test toroidal coordinate helper"""
        cs = coords.toroidal_coords()
        assert len(cs.base_symbols()) == 4  # 4 dim space
        assert str(cs) == "toroidal"

        cs = coords.toroidal_coords(dim=2)
        assert len(cs.base_symbols()) == 2  # 4 dim space
        assert str(cs) == "toroidal"

    def test_cartesian_coords(self):
        """Test cartesian coordinate helper"""
        cs = coords.cartesian_coords()
        assert len(cs.base_symbols()) == 4  # 4 dim space
        assert str(cs) == "cartesian"

        cs = coords.cartesian_coords(dim=2)
        assert len(cs.base_symbols()) == 2  # 4 dim space
        assert str(cs) == "cartesian"


class TestCoordSystem:
    """Test CoordSystem Class"""

    def _dummy_cs(self):
        """Create a dummy CoordSystem"""
        manifold = Manifold('M', 3)
        origin_patch = Patch('o', manifold)
        return coords.CoordSystem('euclidean', origin_patch, ['x', 'y', 'z'])

    def test_create(self):
        """Test creation of CS"""
        cs = self._dummy_cs()
        assert isinstance(cs, coords.CoordSystem)

    def test_base_symbols(self):
        """Test extraction of base symbols"""
        cs = self._dummy_cs()
        coord_syms = cs.base_symbols()
        assert str(coord_syms) == "(x, y, z)"

    def test_from_sympy_coordsystem(self):
        """Test creating from sympy coord system"""
        manifold = Manifold('M', 4)
        origin_patch = Patch('o', manifold)
        sym_cs = _CoordSystem('cartesian', origin_patch, ['x', 'y', 'z'])
        cs = coords.CoordSystem.from_sympy_coordsystem(sym_cs)
        assert isinstance(cs, coords.CoordSystem)

    def test_from_twoform(self):
        """Test from twoform"""
        cs = coords.toroidal_coords(dim=2)
        dt, dr = cs.base_oneforms()
        a, b = symbols('a b')
        form = a * tpow(dt, 2) + b * tpow(dr, 2)
        cs_p = coords.CoordSystem.from_twoform(form)
        assert cs == cs_p
