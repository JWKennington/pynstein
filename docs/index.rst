PyStein Documentation
=====================

The `pystein` package contains utilities for computing symbolic utilities for computing various
quantities that arise in general relativity. Presently, this package is essentially a `sympy` extension that computes
components of tensors directly.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   tutorials/tutorials


Installation
------------

The `pystein` package is available on PyPI, and can be installed via pip, see :doc:`./installation`.



Symbolic Utilities
------------------

The symbolic utilities within `pystein` extend those of `sympy.diffgeom` and are capable of:

* constructing metric tensors in arbitrary coordinates
* computing coefficients of curvature tensors
* computing coefficients of matter tensors
* computing the Einstein equations

For more see the tutorial on the symbolic tools (:doc:`tutorials/symbolic`).

Numeric Utilities
-----------------

The `pystein` package contains some limited numerical utilities, including:

* ability to numerically integrate the geodesic equations `geodesic.numerical_geodesic`
* convenience functions to compute multiple geodesics from a variety of initial conditions (2D)

These utilities are compatible with the symbolic tools thanks to `sympy.lambdify`, which is used to convert symbolic
equations into numeric equations.

For more, see the tutorial on the numeric tools (:doc:`tutorials/numerical`).

.. note::
   The numeric tools in `pystein` are still in beta. For "bad" initial conditions you may encounter warnings and errors
   from numpy and scipy.

Quick Start
-----------

The below code snippet gives a concise example of computing curvature coefficients. For a more explanation on this
snippet see :doc:`quickstart`.

.. code-block:: python

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

For more detail on the symbolic utilities, see :doc:`tutorials/symbolic`.

.. toctree::
   :caption: API Reference
   :maxdepth: 2

   api/pystein

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
