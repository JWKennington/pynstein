"""Unittests for the Symbolic utilities Module
"""

from sympy import symbols, Matrix

from collapse.symbolic import utilities, coords


class TestUtilities:
    """Test utilities Module"""

    def test_tensor_pow(self):
        """Test tensor power"""
        a = symbols('a')
        assert repr(utilities.tensor_pow(a, 1)) == "a"
        assert repr(utilities.tensor_pow(a, 3)) == "a**3"

    def test_matrix_to_twoform(self):
        """Test matrix -> Expr"""
        cs = coords.cartesian_coords(dim=2)
        base_forms = cs.base_oneforms()
        a, b = symbols('a b')
        matrix = Matrix([[a ** 2, 0], [0, b ** 2]])
        form = utilities.matrix_to_twoform(matrix, base_forms)
        assert repr(form) == "a**2*TensorProduct(dt, dt) + b**2*TensorProduct(dx, dx)"
