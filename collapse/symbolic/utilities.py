import functools
from typing import Union

from sympy import Symbol, Array, Rational
from sympy.diffgeom import TensorProduct


def tensor_pow(x, n: int):
    return functools.reduce(TensorProduct, n * [x])


def symbolize(s: Union[str, Symbol]) -> Symbol:
    if isinstance(s, str):
        return Symbol(s)
    return s


def matrix_to_twoform(matrix: Array, base_forms):
    return sum([(1 if i == j else Rational(1, 2)) * TensorProduct(dx_i, dx_j) * matrix[i, j]
                for i, dx_i in enumerate(base_forms) for j, dx_j in enumerate(base_forms)])
