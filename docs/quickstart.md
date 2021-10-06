# Quick Start with `pystein`

This simple example usage of `pystein` will help you get started computing metric coefficients!

## Common Imports

We begin with the necessary imports:

```python
import sympy
from sympy.diffgeom import Manifold, Patch

from pystein import coords, metric, curvature
from pystein.utilities import tensor_pow as tpow
```

## Creating a Metric

We use the example of $S^2$. First we create the manifold and patch object, though these won't be used much
yet `sympy.diffgeom` intends to add features for them later.

```python
M = Manifold('M', dim=2)
P = Patch('origin', M)
```

Define the coordinates for the sphere ($\theta, \phi$), as well as a constant $a$

```python
theta, phi, a = sympy.symbols('theta phi a', nonnegative=True)
cs = coords.CoordSystem('spherical', P, [theta, phi])
```

Next, we extract the one-forms from the coordinate system. We will construct a two-form in terms of these coordinate
one-forms.

```python
dtheta, dphi = cs.base_oneforms()
```

Construct the twoform

```python
ds2 = a ** 2 * (tpow(dtheta, 2) + sympy.sin(theta) ** 2 * tpow(dphi, 2))
```

Last, we construct the `Metric` object:

```python
g = metric.Metric(twoform=ds2)
```

## Compute Curvature Components

Now that we have defined a metric, we can compute curvature components. To compute components individually use the
function ending in `_component` in the `curvature` module that corresponds to the desired curvature tensor. For example:

```python
curvature.christoffel_symbol_component(0, 1, 0, g)
```

The common components can also be computed all at once:

```python
christoffels, riemanns, riccis = curvature.compute_components(g, non_trivial=True)
```

When in a Jupyter environment, the components can be displayed concisely as a single $\LaTeX$ equation:

```python
curvature.display_components(christoffels)
```