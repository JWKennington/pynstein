"""Miscellaneous symbolic utilities"""

import functools
import typing
from typing import Tuple

import pandas
from IPython import display as _display
import sympy
from sympy import Rational, Expr, Matrix, simplify
from sympy.diffgeom import TensorProduct
from sympy.tensor.tensor import Tensor

from pystein import constants


def tensor_pow(x: Tensor, n: int) -> Tensor:
    """Shorthand for computing reflexive tensor products of order n

    Args:
        x:
            Tensor, to be raised to power
        n:
            int, power to raise tensor

    Returns:
        Tensor, T^n
    """
    return functools.reduce(TensorProduct, n * [x])


def matrix_to_twoform(matrix: Matrix, base_forms: Tuple[Expr, ...]) -> Expr:
    """Logical inverse of sympy.diffgeom.twoform_to_matrix

    Args:
        matrix:
            Matrix, the matrix representation of the twoform to produce
        base_forms:
            Tuple[Expr], tuple of oneforms representing a basis of the cotangent bundle

    Returns:
        Expression of the twoform of the matrix in terms of the base oneforms
    """
    return sum([(1 if i == j else Rational(1, 2)) * TensorProduct(dx_i, dx_j) * matrix[i, j]
                for i, dx_i in enumerate(base_forms) for j, dx_j in enumerate(base_forms)])


def clean_expr(e: Expr, natural: bool = True) -> Expr:
    """Helper function to compute clean expression

    Args:
        e:
            Expr, expression to clean

    Returns:
        Expr, cleaned expression
    """
    if natural:
        e = constants.subs_natural(e)
    return simplify(e.doit())


def full_simplify(x):
    return sympy.simplify(sympy.expand(x.simplify()))


def unwrap_latex(s: str) -> str:
    if s.startswith('$\\displaystyle '):
        s = s.replace('$\\displaystyle ', '')
    if s.startswith('$') or s.endswith('$'):
        s = s.replace('$', '')
    return s


def wrap_latex(s: str, style: str = '') -> str:
    return '{}{}{}{}'.format('' if s.startswith('$') else '$',
                             style,
                             s,
                             '' if s.endswith('$') else '$')


def concat_latex(exprs: typing.List[sympy.Expr], labels: typing.List[str] = None, label_names: typing.List[str] = None, display=False):
    latex_exprs = [unwrap_latex(full_simplify(e)._repr_latex_()) for e in exprs]
    if labels is not None and label_names is not None:
        label_strs = ['({})'.format(', '.join('{}={:d}'.format(name, value) for name, value in zip(label_names, label))) for label in labels ]
    else:
        label_strs = len(exprs) * ['']
    combined = '\\begin{{split}} {} \\end{{split}}'.format(' \\\\ '.join('{} &: {}'.format(label, expr) for label, expr in zip(label_strs, latex_exprs)))
    tex = wrap_latex(combined)

    if display:
        _display.display_latex(tex, raw=True)
    return tex


def boundary_filter(df: pandas.DataFrame, **kwargs):
    queries = []
    for k, v in sorted(kwargs.items(), key=lambda x: x[0]):
        queries.append('{col} >= {min_} and {col} <= {max_}'.format(col=k,
                                                                    min_=v[0],
                                                                    max_=v[1]))
    query = ' and '.join(queries)
    return df.query(query)

