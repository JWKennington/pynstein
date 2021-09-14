"""Utilities for constructing a metric

"""

import functools
import itertools
from typing import Tuple, Union, List

import sympy
from sympy import Function, sin, Expr, Array, Derivative as D, MatrixBase, Matrix, Symbol
from sympy.diffgeom import twoform_to_matrix
from sympy.printing.latex import latex

from pystein import coords, symbols
from pystein import constants
from pystein.constants import c
from pystein.utilities import tensor_pow as tpow, matrix_to_twoform


class Metric:
    """Metric represents a twoform on a manifold that is symmetric. This class is capable of being
    created from and converted to both twoform notation and matrix notation given a coordinate system.
    """

    def __init__(self, twoform: Expr = None, matrix: Array = None, coord_system: coords.CoordSystem = None,
                 components: Tuple[Expr, ...] = None):
        """Create a Metric"""
        if twoform is None and matrix is None:
            raise ValueError('Must specify either twoform or matrix to produce metric')

        # Construct twoform if none given
        if twoform is None:
            if not isinstance(matrix, MatrixBase):
                matrix = Matrix(matrix)
            if coord_system is None:
                raise ValueError('Must specify coord system if constructing metric from matrix')
            twoform = matrix_to_twoform(matrix, coord_system.base_oneforms())  # TODO check ordering of base oneforms?

        # Construct matrix if none given
        if matrix is None:
            matrix = twoform_to_matrix(twoform)
            coord_system = coords.CoordSystem.from_twoform(twoform)

        # Set instance attributes
        self._twoform = twoform
        self._matrix = matrix
        self._inverse = None  # lazy caching of inverse matrix
        self.coord_system = coord_system
        self.components = components

    def __repr__(self):
        """String repr"""
        return repr(self.twoform)

    def _repr_latex_(self):
        """LaTeX repr in Jupyter"""
        s = latex(self.twoform, mode='plain')
        return "$\\displaystyle %s$" % s

    @property
    def twoform(self):
        """Safe accessor for twoform"""
        return self._twoform

    @property
    def matrix(self):
        """Safe accessor for matrix"""
        return self._matrix

    @property
    def inverse(self):  # TODO include method parameters in here, for instance pseudo inverse
        """Compute the inverse metric (if possible) and return new Metric instance"""
        if self._inverse is None:
            self._inverse = self.matrix.inv()  # only compute once
        return Metric(matrix=self._inverse, coord_system=self.coord_system, components=self.components)

    def subs(self, *args, **kwargs):
        """Pass thru to twoform substitution"""
        return Metric(twoform=self.twoform.subs(*args, **kwargs),
                      # TODO make the filtering below more robust
                      components=tuple(c for c in self.components if not c.subs(*args, **kwargs).doit().is_constant()))

    def inner_product(self, vec1: List[sympy.Expr], vec2: List[sympy.Expr]):
        N = len(self.coord_system.base_symbols())

        res = 0

        for mu in range(N):
            for nu in range(N):
                res += self._matrix[mu, nu] * vec1[mu] * vec2[nu]

        return res

    def norm(self, vec: List[sympy.Expr]):
        return sympy.sqrt(self.inner_product(vec, vec))


    def angle(self, vec1, vec2):
        norm_ip = self.inner_product(vec1, vec2) / self.norm(vec1) / self.norm(vec2)
        return sympy.acos(norm_ip)



def minkowski():
    """Utility for constructing the Minkowski metric

    Returns:
        Metric, the Minkowski metric for flat space

    References:
        [1] S. Weinberg, Cosmology (Oxford University Press, Oxford ; New York, 2008).
    """
    cs = coords.cartesian_coords()
    dt, dx, dy, dz = cs.base_oneforms()
    form = - tpow(dt, 2) + tpow(dx, 2) + tpow(dy, 2) + tpow(dz, 2)
    return Metric(twoform=form)


def friedmann_lemaitre_roberston_walker(curvature_constant: Symbol = symbols.k, cartesian: bool = False):
    """Utility for constructing the FLRW metric in terms of a unit lapse and general
    scale function `a`.

    Args:
        curvature_constant:
            Symbol, default "k", the curvature parameter in reduced polar coordinates
        cartesian:
            bool, default False. If true create a cartesian FLRW and ignore curvature_constant argument

    Returns:
        Metric, the FLRW metric

    References:
        [1] S. Weinberg, Cosmology (Oxford University Press, Oxford ; New York, 2008).
    """
    a = Function('a')(symbols.t)
    if cartesian:
        cs = coords.cartesian_coords()
        dt, dx, dy, dz = cs.base_oneforms()
        form = - c ** 2 * tpow(dt, 2) + a ** 2 * (tpow(dx, 2) + tpow(dy, 2) + tpow(dz, 2))
    else:
        cs = coords.toroidal_coords()
        _, r, theta, _ = cs.base_symbols()
        dt, dr, dtheta, dphi = cs.base_oneforms()
        form = - c ** 2 * tpow(dt, 2) + a ** 2 * (1 / (1 - curvature_constant * r ** 2) * tpow(dr, 2) + r ** 2 * (tpow(dtheta, 2) + sin(theta) ** 2 * tpow(dphi, 2)))
    return Metric(twoform=form, components=(a,))


flrw = friedmann_lemaitre_roberston_walker  # shorthand for conventional names


def general_inhomogeneous_isotropic(use_natural_units: bool = True):
    """Utility for constructing a general inhomogeneous, but still isotropic, metric (GIIM). The metric
    components M, N, L, S all depend on time and radius, but not theta or phi (hence isotropy).

    Returns:
        Metric, the GIIM metric
    """
    cs = coords.toroidal_coords()
    t, r, theta, _ = cs.base_symbols()
    dt, dr, dtheta, dphi = cs.base_oneforms()

    # Create generic isotropic metric component functions
    M = Function('M')(t, r)
    N = Function('N')(t, r)
    L = Function('L')(t, r)
    S = Function('S')(t, r)

    form = - c ** 2 * N ** 2 * tpow(dt, 2) + \
           L ** 2 * tpow(dr + c * M * dt, 2) + \
           S ** 2 * (tpow(dtheta, 2) + sin(theta) ** 2 * tpow(dphi, 2))
    if use_natural_units:
        form = constants.subs_natural(form)
    return Metric(twoform=form, components=(M, N, L, S))


gii = general_inhomogeneous_isotropic  # shorthand for conventional names


def _deriv_simplify_rule(component: Function, variables: Union[Expr, Tuple[Expr, ...]], use_dots: bool = False):
    """Helper function for simplifying derivative notation"""
    if not isinstance(variables, tuple):  # TODO make this "boxing" more robust
        variables = (variables,)
    args = component.args
    order = len(variables)
    key = functools.reduce(D, (component,) + variables)

    if any(v not in args for v in variables):  # check against simplified
        return (key, 0)

    if len(args) == 1:
        fmt = ('\\' + order * 'd' + 'ot{{{}}}') if use_dots else ('{}' + order * '\'')
        return (key, Function(fmt.format(component.name))(*args))
    fmt = '{}_' + '{{' + ' '.join([v.name for v in variables]) + '}}'
    return (key, Function(fmt.format(component.name))(*args))


def simplify_deriv_notation(expr: Expr, metric: Metric, max_order: int = 2, use_dots: bool = False):
    """Utility for Simplifying LaTeX representation of a sympy Expression via substitutions. Note
    that this function simplifies the LaTeX output of the Expr at the cost of the Expr semantics,
    only use this after all operations on the Expr (including simplification) have been performed.

    Args:
        expr:
            Expr, the sympy expression
        metric:
            Metric, the metric containing components whose derivatives will be simplified
        max_order:
            int, default 2, the max derivative order to replace
        use_dots:
            bool, default False. If True use dot notation for derivatives of single-variable functions

    Returns:
        Expr, the modified expression. Recall this is only useful for LaTeX conversion, not semantically valid in sympy.
    """
    # Create Simplification Shorthand
    components = tuple(sorted(metric.components, key=lambda x: x.name))
    variables = metric.coord_system.base_symbols()
    rules = []
    for n in range(1, max_order + 1):
        n_order_rules = [_deriv_simplify_rule(c, vs, use_dots=use_dots) for c, vs in
                         itertools.product(components, itertools.product(*(n * [variables])))]
        rules.extend(n_order_rules)
    return expr.subs(dict(rules))
