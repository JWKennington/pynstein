"""Unittests for the Symbolic utilities Module
"""

from sympy import symbols, Matrix, Function, Derivative

from pystein import coords
from pystein import utilities


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

    def test_clean_expr(self):
        """Test"""
        a, b, c = symbols('a b c')
        f = Function('f')(a, b)
        g = Derivative(f, a) + Derivative(f, c)
        c = g ** 2 + 1 / b
        assert str(c) == '(Derivative(f(a, b), a) + Derivative(f(a, b), c))**2 + 1/b'
        assert str(utilities.clean_expr(c)) == 'Derivative(f(a, b), a)**2 + 1/b'
