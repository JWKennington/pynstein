# General Relativity Symbolic Utilities

[![PyPI version](https://img.shields.io/pypi/v/pystein)](https://pypi.org/project/pystein/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pystein)](https://pypi.org/project/pystein/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/pystein)](https://pypi.org/project/pystein/)
[![Build](https://github.com/JWKennington/pynstein/actions/workflows/build.yml/badge.svg)](https://github.com/JWKennington/pynstein/actions/workflows/build.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/jwkennington/pystein/badge)](https://www.codefactor.io/repository/github/jwkennington/pystein)
[![codecov](https://codecov.io/gh/JWKennington/pystein/branch/main/graph/badge.svg?token=2XRgGH05zb)](https://codecov.io/gh/JWKennington/pystein)
[![License](https://img.shields.io/pypi/l/pystein?color=magenta)](https://pypi.org/project/pystein/)


The `pystein` package contains utilities for computing symbolic utilities for computing various 
quantities that arise in general relativity. Presently, this package is essentially a `sympy` extension that computes 
components of tensors directly.


## Installation

The `pystein` package is available on PyPI, and can be installed via pip:

```bash
pip install pystein
```

## Symbolic Tools

The `pystein` package makes use of `sympy` to compute symbolic curvature equations (EFE). A sample
snippet is below. For more detail see the [documentation](https://pystein.readthedocs.io/en/latest/).

```python
# Imports
import sympy
from sympy.diffgeom import Manifold, Patch
from pystein import coords, metric, curvature
from pystein.utilities import tensor_pow as tpow

# Create metric
M = Manifold('M', dim=2)
P = Patch('origin', M)
theta, phi, a = sympy.symbols('theta phi a', nonnegative=True)
cs = coords.CoordSystem('spherical', P, [theta, phi])
dtheta, dphi = cs.base_oneforms()
ds2 = a ** 2 * (tpow(dtheta, 2) + sympy.sin(theta) ** 2 * tpow(dphi, 2))
g = metric.Metric(twoform=ds2)

# Compute Christoffel Component
curvature.christoffel_symbol_component(0, 1, 0, g)
```






## Numeric Tools

The `pystein` package contains some limited numerical utilities, including:

- ability to numerically integrate the geodesic equations `geodesic.numerical_geodesic`
- convenience functions to compute multiple geodesics from a variety of initial conditions (2D)

These utilities are compatible with the symbolic tools thanks to `sympy.lambdify`, which is used to convert symbolic
equations into numeric equations.

*Note that the numeric tools in `pystein` are still in beta.

