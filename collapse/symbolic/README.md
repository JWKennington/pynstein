# Symbolic Tools

## Coordinate Systems

```python
from sympy.diffgeom import Manifold, Patch
from collapse.symbolic import coords
```

```python
# The collapse CoordinateSystem extends the sympy.diffgeom api to make parameters more accessible
M = Manifold('M', dim=2)
P = Patch('origin', M)
cs = coords.CoordSystem('cartesian', P, ['x', 'y'])
cs
```

$\text{OneDim}^{\text{origin}}_{\text{M}}$

```python
# In sympy it is difficult to access underlying parameters, but the new base_symbols function makes it easy:
cs.base_symbols()
```

$\left( t, \  x\right)$

## Metrics

```python
# Assembling a metric is easy
from sympy import Array, symbols
from collapse.symbolic import metric
from collapse.symbolic.utilities import tensor_pow as tpow
```

```python
# Metrics can be created either from a (Matrix, Coords) combo or from a TwoForm Expression
# Let's create a metric from a twoform expression, using the basis of oneforms from the coordinate system
a, b = symbols('a b') # some constants to use in the metric
dx, dy = cs.base_oneforms()
form = a**2 * tpow(dx, 2) + b**2 * tpow(dy, 2)
g1 = metric.Metric(twoform=form) # Note: don't have to specify coords since implied by basis of one-forms
```

```python
# Notice that the Metric class will represent itself as a twoform
g1
```

$a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$

```python
# Now let's create the same metric from a matrix
# First let's create a Matrix
matrix = Array([[a**2, 0], [0, b**2]])
matrix
```

$\left[\begin{matrix}a^{2} & 0\\0 & b^{2}\end{matrix}\right]$

```python
# Creating a Metric from a matrix also requires you to specify the coordinate system (so the axes can be labeled)
g2 = metric.Metric(matrix=matrix, coord_system=cs)
```

```python
# Note that the Metric class automatically computes the two-form and uses it for representation
g2
```

$a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$

```python
# Metrics can be inverted, and produce other metrics
g3 = g2.inverse
g3
```

$\frac{\operatorname{d}y \otimes \operatorname{d}y}{b^{2}} + \frac{\operatorname{d}x \otimes \operatorname{d}x}{a^{2}}$

## Curvature

```python
# Now let's compute curvature terms
from sympy import Function
from collapse.symbolic import curvature
```

```python
# Let's create a metric with some curvature..
x, y = cs.base_symbols() # grab the coordinate parameters
F = Function('F')(x, y) # Define an arbitrary function that depends on x and y
g4 = metric.Metric(twoform=F**2 * tpow(dx, 2) + b**2 * tpow(dy, 2))
```

```python
curvature.ricci_tensor_component(0, 0, g4).doit()
```

$- \frac{F{\left(x,y \right)} \frac{\partial^{2}}{\partial y^{2}} F{\left(x,y \right)}}{b^{2}}$


## Matter

```python
# Let's compute the matter stress energy tensor of a perfect fluid in 1D
from collapse.symbolic import matter
```

```python
# Need to quickly redefine the coordinates to have a temporal coordinate
M = Manifold('M', dim=2)
P = Patch('origin', M)
cs = coords.CoordSystem('OneDim', P, ['t', 'x'])

t, x = cs.base_symbols()
dt, dx = cs.base_oneforms()
Q = Function('Q')(t, x) # Define an arbitrary function that depends on x and y
g5 = metric.Metric(twoform=- Q**2 * tpow(dt, 2) + b**2 * tpow(dx, 2), components=(Q, b))
g5
```

$b^{2} \operatorname{d}x \otimes \operatorname{d}x - Q^{2}{\left(t,x \right)} \operatorname{d}t \otimes \operatorname{d}t$

```python
# Now use the matter module to create the stress energy tensor for perfect fluid
T = matter.perfect_fluid_stress_energy(g5)
T
```

$\left[\begin{matrix}p - \frac{p}{Q^{2}{\left(t,x \right)}} + \rho & 0\\0 & \frac{p}{b^{2}}\end{matrix}\right]$

```python
curvature.einstein_tensor_component(0, 0, g5).doit()
```

$\frac{Q^{2}{\left(t,x \right)}}{2} + \frac{Q{\left(t,x \right)} \frac{\partial^{2}}{\partial x^{2}} Q{\left(t,x \right)}}{b^{2}}$

```python
# Note that in the limit Q -> 1
g5_lim = g5.subs({Q: 1})
T_lim = matter.perfect_fluid_stress_energy(g5_lim)
T_lim
```

$\left[\begin{matrix}\rho & 0\\0 & \frac{p}{b^{2}}\end{matrix}\right]$

```python
curvature.einstein_tensor_component(0, 0, g5_lim).doit()
```

$\frac{1}{2}$

## Gravity

```python
# One can also directly compute the Einstein Equations
from collapse.symbolic import gravity
```

```python
gravity.einstein_equation(0, 0, g5).doit()
```

$\frac{Q^{2}{\left(t,x \right)}}{2} + \frac{Q{\left(t,x \right)} \frac{\partial^{2}}{\partial x^{2}} Q{\left(t,x \right)}}{b^{2}} = p - \frac{p}{Q^{2}{\left(t,x \right)}} + \rho$

```python
# Similarly in the limit:
gravity.einstein_equation(0, 0, g5_lim).doit()
```

$\frac{1}{2} = \rho$

## Full Example: FLRW Cosmology

```python
# Load the predefined FLRW metric
flrw = metric.flrw_metric().subs({'c': 1})
flrw
```

$a{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right) - \operatorname{d}t \otimes \operatorname{d}t$

```python
efe_00 = gravity.einstein_equation(0, 0, flrw).doit()
efe_00
```

$\frac{1}{2} - \frac{3 \frac{d^{2}}{d t^{2}} a{\left(t \right)}}{2 a{\left(t \right)}} + \frac{3 \left(\frac{d}{d t} a{\left(t \right)}\right)^{2}}{4 a^{2}{\left(t \right)}} = \rho$

```python
# Simplify derivative notation:
metric.simplify_deriv_notation(efe_00, flrw)
```

$\frac{1}{2} - \frac{3 \operatorname{a''}{\left(t \right)}}{2 a{\left(t \right)}} + \frac{3 \operatorname{a'}^{2}{\left(t \right)}}{4 a^{2}{\left(t \right)}} = \rho$

```python
# Can also use "dots"
metric.simplify_deriv_notation(efe_00, flrw, use_dots=True)
```

$- \frac{3 \ddot{a}{\left(t \right)}}{2 a{\left(t \right)}} + \frac{3 \dot{a}^{2}{\left(t \right)}}{4 a^{2}{\left(t \right)}} + \frac{1}{2} = \rho$




