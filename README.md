# General Relativity Symbolic Utilities

[![PyPI version](https://img.shields.io/pypi/v/pystein)](https://pypi.org/project/pystein/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pystein)](https://pypi.org/project/pystein/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/pystein)](https://pypi.org/project/pystein/)
[![Build](https://github.com/JWKennington/pynstein/actions/workflows/build.yml/badge.svg)](https://github.com/JWKennington/pynstein/actions/workflows/build.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/jwkennington/pystein/badge)](https://www.codefactor.io/repository/github/jwkennington/pystein)
[![codecov](https://codecov.io/gh/JWKennington/pynstein/branch/main/graph/badge.svg?token=2XRgGH05zb)](https://codecov.io/gh/JWKennington/pynstein)
[![License](https://img.shields.io/pypi/l/pystein?color=magenta)](https://pypi.org/project/pystein/)


The `pystein` package contains utilities for computing symbolic utilities for computing various 
quantities that arise in general relativity. Presently, this package is essentially a `sympy` extension that computes 
components of tensors directly.


## Symbolic Tools

The `pystein` package makes use of `sympy` to compute symbolic curvature equations (EFE).

### Example Computation: FLRW Cosmology

```python
# Load the predefined FLRW metric
from pystein import metric, gravity
from pystein import utilities

flrw = metric.flrw().subs({'c': 1})
flrw
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" title="\large \displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)" /></a>
<!-- $\displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)$ -->

```python
efe_00 = utilities.full_simplify(gravity.einstein_equation(0, 0, flrw))
efe_00
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\frac{3&space;\left(\frac{d}{d&space;t}&space;a{\left(t&space;\right)}\right)^{2}}{a^{2}{\left(t&space;\right)}}&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\frac{3&space;\left(\frac{d}{d&space;t}&space;a{\left(t&space;\right)}\right)^{2}}{a^{2}{\left(t&space;\right)}}&space;=&space;0" title="\large \displaystyle \frac{3 \left(\frac{d}{d t} a{\left(t \right)}\right)^{2}}{a^{2}{\left(t \right)}} = 0" /></a>
<!-- $\displaystyle \frac{3 \left(\frac{d}{d t} a{\left(t \right)}\right)^{2}}{a^{2}{\left(t \right)}} = 0$ -->

```python
# Can simplify notation using "dots"
metric.simplify_deriv_notation(efe_00, flrw, use_dots=True)
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\frac{3&space;\dot{a}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\frac{3&space;\dot{a}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}&space;=&space;0" title="\large \displaystyle \frac{3 \dot{a}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}} = 0" /></a>
<!-- $\displaystyle \frac{3 \dot{a}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}} = 0$ -->

# Symbolic Tools

## Coordinate Systems

```python
from sympy.diffgeom import Manifold, Patch
from pystein import coords
```

```python
# The pystein CoordinateSystem extends the sympy.diffgeom api to make parameters more accessible
M = Manifold('M', dim=2)
P = Patch('origin', M)
cs = coords.CoordSystem('cartesian', P, ['x', 'y'])
cs
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\text{cartesian}^{\text{origin}}_{\text{M}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\text{cartesian}^{\text{origin}}_{\text{M}}" title="\large \displaystyle \text{cartesian}^{\text{origin}}_{\text{M}}" /></a>
<!-- $\displaystyle \text{cartesian}^{\text{origin}}_{\text{M}}$ -->

```python
# In sympy it is difficult to access underlying parameters, but the new base_symbols function makes it easy:
cs.base_symbols()
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\left(&space;x,&space;\&space;y\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\left(&space;x,&space;\&space;y\right)" title="\large \left( x, \ y\right)" /></a>
<!-- $\left( x, \  y\right)$ -->

## Metrics

```python
# Assembling a metric is easy
from sympy import Array, symbols
from pystein import metric
from pystein.utilities import tensor_pow as tpow
```

```python
# Metrics can be created either from a (Matrix, Coords) combo or from a TwoForm Expression
# Let's create a metric from a twoform expression, using the basis of oneforms from the coordinate system
a, b = symbols('a b')  # some constants to use in the metric
dx, dy = cs.base_oneforms()
form = a ** 2 * tpow(dx, 2) + b ** 2 * tpow(dy, 2)
g1 = metric.Metric(twoform=form)  # Note: don't have to specify coords since implied by basis of one-forms
```

```python
# Notice that the Metric class will represent itself as a twoform
g1
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" title="\large a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y" /></a>
<!-- $a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$ -->

```python
# Now let's create the same metric from a matrix
# First let's create a Matrix
matrix = Array([[a ** 2, 0], [0, b ** 2]])
matrix
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\left[\begin{matrix}a^{2}&space;&&space;0\\0&space;&&space;b^{2}\end{matrix}\right]" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\left[\begin{matrix}a^{2}&space;&&space;0\\0&space;&&space;b^{2}\end{matrix}\right]" title="\left[\begin{matrix}a^{2} & 0\\0 & b^{2}\end{matrix}\right]" /></a>
<!-- $\left[\begin{matrix}a^{2} & 0\\0 & b^{2}\end{matrix}\right]$ -->

```python
# Creating a Metric from a matrix also requires you to specify the coordinate system (so the axes can be labeled)
g2 = metric.Metric(matrix=matrix, coord_system=cs)
```

```python
# Note that the Metric class automatically computes the two-form and uses it for representation
g2
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" title="\large a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y" /></a>
<!-- $a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$ -->

```python
# Metrics can be inverted, and produce other metrics
g3 = g2.inverse
g3
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\frac{\operatorname{d}y&space;\otimes&space;\operatorname{d}y}{b^{2}}&space;&plus;&space;\frac{\operatorname{d}x&space;\otimes&space;\operatorname{d}x}{a^{2}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\frac{\operatorname{d}y&space;\otimes&space;\operatorname{d}y}{b^{2}}&space;&plus;&space;\frac{\operatorname{d}x&space;\otimes&space;\operatorname{d}x}{a^{2}}" title="\large \frac{\operatorname{d}y \otimes \operatorname{d}y}{b^{2}} + \frac{\operatorname{d}x \otimes \operatorname{d}x}{a^{2}}" /></a>
<!-- $\frac{\operatorname{d}y \otimes \operatorname{d}y}{b^{2}} + \frac{\operatorname{d}x \otimes \operatorname{d}x}{a^{2}}$ -->

## Curvature

```python
# Now let's compute curvature terms
from sympy import Function
from pystein import curvature
```

```python
# Let's create a metric with some curvature..
x, y = cs.base_symbols()  # grab the coordinate parameters
F = Function('F')(x, y)  # Define an arbitrary function that depends on x and y
g4 = metric.Metric(twoform=F ** 2 * tpow(dx, 2) + b ** 2 * tpow(dy, 2))
```

```python
curvature.ricci_tensor_component(0, 0, g4).doit()
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;-&space;\frac{F{\left(x,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;y^{2}}&space;F{\left(x,y&space;\right)}}{b^{2}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;-&space;\frac{F{\left(x,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;y^{2}}&space;F{\left(x,y&space;\right)}}{b^{2}}" title="\large - \frac{F{\left(x,y \right)} \frac{\partial^{2}}{\partial y^{2}} F{\left(x,y \right)}}{b^{2}}" /></a>
<!-- $- \frac{F{\left(x,y \right)} \frac{\partial^{2}}{\partial y^{2}} F{\left(x,y \right)}}{b^{2}}$ -->

## Matter

```python
# Let's compute the matter stress energy tensor of a perfect fluid in 1D
from pystein import matter
```

```python
# Need to quickly redefine the coordinates to have a temporal coordinate
t, x, y = symbols('t x y')
M = Manifold('M', dim=3)
P = Patch('origin', M)
cs = coords.CoordSystem('OneDim', P, [t, x, y])

dt, dx, dy = cs.base_oneforms()
Q = Function('Q')(t, y)  # Define an arbitrary function that depends on x and y
S = Function('S')(t, x)  # Define an arbitrary function that depends on x and y
g5 = metric.Metric(twoform=- Q ** 2 * tpow(dt, 2) + b ** 2 * tpow(dx, 2) + S ** 2 * tpow(dy, 2), components=(Q, S, b))
g5
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;b^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;-&space;Q^{2}{\left(t,y&space;\right)}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;S^{2}{\left(t,x&space;\right)}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;b^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;-&space;Q^{2}{\left(t,y&space;\right)}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;S^{2}{\left(t,x&space;\right)}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" title="\large \displaystyle b^{2} \operatorname{d}x \otimes \operatorname{d}x - Q^{2}{\left(t,y \right)} \operatorname{d}t \otimes \operatorname{d}t + S^{2}{\left(t,x \right)} \operatorname{d}y \otimes \operatorname{d}y" /></a>
<!-- $\displaystyle b^{2} \operatorname{d}x \otimes \operatorname{d}x - Q^{2}{\left(t,y \right)} \operatorname{d}t \otimes \operatorname{d}t + S^{2}{\left(t,x \right)} \operatorname{d}y \otimes \operatorname{d}y$ -->

```python
# Now use the matter module to create the stress energy tensor for perfect fluid
T = matter.perfect_fluid(g5)
T
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" title="\large \displaystyle \left[\begin{matrix}\rho - p Q^{2}{\left(t,y \right)} + p & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]" /></a>
<!-- $\displaystyle \left[\begin{matrix}\rho - p Q^{2}{\left(t,y \right)} + p & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]$ -->

```python
utilities.clean_expr(curvature.einstein_tensor_component(0, 0, g5))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->

```python
# Note that in the limit Q -> 1
g5_lim = g5.subs({Q: 1})
T_lim = matter.perfect_fluid(g5_lim)
T_lim
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" title="\large \displaystyle \left[\begin{matrix}\rho & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]" /></a>
<!-- $\displaystyle \left[\begin{matrix}\rho & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]$ -->

```python
utilities.clean_expr(curvature.einstein_tensor_component(0, 0, g5_lim))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;\frac{\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;\frac{\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle - \frac{\frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle - \frac{\frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->

## Gravity

```python
# One can also directly compute the Einstein Equations
from pystein import gravity
```

```python
utilities.clean_expr(gravity.einstein_equation(0, 0, g5, T))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\left(\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p\right)&space;=&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\left(\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p\right)&space;=&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle 8 \pi \left(\rho - p Q^{2}{\left(t,y \right)} + p\right) = - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle 8 \pi \left(\rho - p Q^{2}{\left(t,y \right)} + p\right) = - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->

```python
# Similarly in the limit:
utilities.clean_expr(gravity.einstein_equation(0, 0, g5_lim, T_lim))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;-&space;\frac{\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;-&space;\frac{\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle 8 \pi \rho = - \frac{\frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle 8 \pi \rho = - \frac{\frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->

## Full Example: FLRW Cosmology

```python
# Load the predefined FLRW metric
flrw = metric.flrw(cartesian=True)
flrw
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" title="\large \displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)" /></a>
<!-- $\displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)$ -->

```python
T = matter.perfect_fluid(flrw)
efe_00 = utilities.clean_expr(gravity.einstein_equation(0, 0, flrw, T).doit())
efe_00
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\left(\frac{d}{d&space;t}&space;a{\left(t&space;\right)}\right)^{2}}{a^{2}{\left(t&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\left(\frac{d}{d&space;t}&space;a{\left(t&space;\right)}\right)^{2}}{a^{2}{\left(t&space;\right)}}" title="\large \displaystyle 8 \pi \rho = \frac{3 \left(\frac{d}{d t} a{\left(t \right)}\right)^{2}}{a^{2}{\left(t \right)}}" /></a>
<!-- $\displaystyle 8 \pi \rho = \frac{3 \left(\frac{d}{d t} a{\left(t \right)}\right)^{2}}{a^{2}{\left(t \right)}}$ -->

```python
# Simplify derivative notation:
metric.simplify_deriv_notation(efe_00, flrw)
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\operatorname{a'}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\operatorname{a'}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}" title="\large \displaystyle 8 \pi \rho = \frac{3 \operatorname{a'}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}}" /></a>
<!-- $\displaystyle 8 \pi \rho = \frac{3 \operatorname{a'}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}}$ -->

```python
# Can also use "dots"
metric.simplify_deriv_notation(efe_00, flrw, use_dots=True)
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\dot{a}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\rho&space;=&space;\frac{3&space;\dot{a}^{2}{\left(t&space;\right)}}{a^{2}{\left(t&space;\right)}}" title="\large \displaystyle 8 \pi \rho = \frac{3 \dot{a}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}}" /></a>
<!-- $\displaystyle 8 \pi \rho = \frac{3 \dot{a}^{2}{\left(t \right)}}{a^{2}{\left(t \right)}}$ -->

## Numeric Tools

The `pystein` package contains some limited numerical utilities, including:

- ability to numerically integrate the geodesic equations `geodesic.numerical_geodesic`
- convenience functions to compute multiple geodesics from a variety of initial conditions (2D)

These utilities are compatible with the symbolic tools thanks to `sympy.lambdify`, which is used to convert symbolic
equations into numeric equations.

*Note that the numeric tools in `pystein` are still in beta.

### Example Geodesic Usage

Construct a metric from a twoform

```python
M = Manifold('M', dim=2)
P = Patch('origin', M)

rho, phi, a = sympy.symbols('rho phi a', nonnegative=True)
cs = coords.CoordSystem('schw', P, [rho, phi])
drho, dphi = cs.base_oneforms()
ds2 = a ** 2 * ((1 / (1 - rho ** 2)) * tpow(drho, 2) + rho ** 2 * tpow(dphi, 2))
g = metric.Metric(twoform=ds2)
g
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\displaystyle&space;a^{2}&space;\left(\rho^{2}&space;\operatorname{d}\phi&space;\otimes&space;\operatorname{d}\phi&space;&plus;&space;\frac{\operatorname{d}\rho&space;\otimes&space;\operatorname{d}\rho}{1&space;-&space;\rho^{2}}\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\displaystyle&space;a^{2}&space;\left(\rho^{2}&space;\operatorname{d}\phi&space;\otimes&space;\operatorname{d}\phi&space;&plus;&space;\frac{\operatorname{d}\rho&space;\otimes&space;\operatorname{d}\rho}{1&space;-&space;\rho^{2}}\right)" title="\displaystyle a^{2} \left(\rho^{2} \operatorname{d}\phi \otimes \operatorname{d}\phi + \frac{\operatorname{d}\rho \otimes \operatorname{d}\rho}{1 - \rho^{2}}\right)" /></a>

Compute the symbolic geodesic equations

```python
full_simplify(geodesic.geodesic_equation(0, sympy.symbols('lambda'), g))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\displaystyle&space;\frac{\left(\rho^{2}{\left(\lambda&space;\right)}&space;-&space;1\right)&space;\left(\rho^{3}{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\phi{\left(\lambda&space;\right)}\right)^{2}&space;-&space;\rho{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\phi{\left(\lambda&space;\right)}\right)^{2}&space;&plus;&space;\frac{d^{2}}{d&space;\lambda^{2}}&space;\rho{\left(\lambda&space;\right)}\right)&space;-&space;\rho{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\rho{\left(\lambda&space;\right)}\right)^{2}}{\rho^{2}{\left(\lambda&space;\right)}&space;-&space;1}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\displaystyle&space;\frac{\left(\rho^{2}{\left(\lambda&space;\right)}&space;-&space;1\right)&space;\left(\rho^{3}{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\phi{\left(\lambda&space;\right)}\right)^{2}&space;-&space;\rho{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\phi{\left(\lambda&space;\right)}\right)^{2}&space;&plus;&space;\frac{d^{2}}{d&space;\lambda^{2}}&space;\rho{\left(\lambda&space;\right)}\right)&space;-&space;\rho{\left(\lambda&space;\right)}&space;\left(\frac{d}{d&space;\lambda}&space;\rho{\left(\lambda&space;\right)}\right)^{2}}{\rho^{2}{\left(\lambda&space;\right)}&space;-&space;1}" title="\displaystyle \frac{\left(\rho^{2}{\left(\lambda \right)} - 1\right) \left(\rho^{3}{\left(\lambda \right)} \left(\frac{d}{d \lambda} \phi{\left(\lambda \right)}\right)^{2} - \rho{\left(\lambda \right)} \left(\frac{d}{d \lambda} \phi{\left(\lambda \right)}\right)^{2} + \frac{d^{2}}{d \lambda^{2}} \rho{\left(\lambda \right)}\right) - \rho{\left(\lambda \right)} \left(\frac{d}{d \lambda} \rho{\left(\lambda \right)}\right)^{2}}{\rho^{2}{\left(\lambda \right)} - 1}" /></a>

Numerically integrate the geodesic equations

```python
init = (numpy.sin(numpy.pi / 4), 0.0, numpy.cos(numpy.pi / 4), numpy.pi / 4)
lambdas = numpy.arange(0, 2.1, 0.001)
df = geodesic.numerical_geodesic(g, init, lambdas)
df.head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rho</th>
      <th>phi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.707107</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.707814</td>
      <td>0.000785</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.708520</td>
      <td>0.001568</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.709226</td>
      <td>0.002349</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.709931</td>
      <td>0.003129</td>
    </tr>
  </tbody>
</table>
</div>


