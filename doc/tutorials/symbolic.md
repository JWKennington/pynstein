```{_tutorial_symbolic}
```
# Tutorial: Symbolic Tools

This tutorial demonstrates in detail how to use the symbolic tools in `pystein`. For other tutorials 
see [all tutorials](tutorials.md).

## Coordinate Systems

The `pystein` `CoordinateSystem` extends the sympy.diffgeom api to make parameters more accessible. This is important 
when computing partial derivatives.[^1] 

```python
from sympy.diffgeom import Manifold, Patch
from pystein import coords
```

For example, a two-dimensional set of coordinates can be created (similarly to sympy.diffgeom.CoordSystem):

```python
M = Manifold('M', dim=2)
P = Patch('origin', M)
cs = coords.CoordSystem('cartesian', P, ['x', 'y'])
cs
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\text{cartesian}^{\text{origin}}_{\text{M}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\text{cartesian}^{\text{origin}}_{\text{M}}" title="\large \displaystyle \text{cartesian}^{\text{origin}}_{\text{M}}" /></a>
<!-- $\displaystyle \text{cartesian}^{\text{origin}}_{\text{M}}$ -->

In sympy it is difficult to access underlying parameters, but the new `base_symbols` method makes it easy:

```python
cs.base_symbols()
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\left(&space;x,&space;\&space;y\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\left(&space;x,&space;\&space;y\right)" title="\large \left( x, \ y\right)" /></a>
<!-- $\left( x, \  y\right)$ -->

## Metrics

Assembling a metric with `pystein` is easy! Metrics can be created either from a (`Matrix`, `Coords`) combo 
or from a `TwoForm` expression constucted from the coordinate system's `base_oneforms`.  

```python
from sympy import Array, symbols
from pystein import metric
from pystein.utilities import tensor_pow as tpow
```

Let's create a metric from a twoform expression, using the basis of oneforms from the coordinate system:

```python
a, b = symbols('a b')  # some constants to use in the metric
dx, dy = cs.base_oneforms()
form = a ** 2 * tpow(dx, 2) + b ** 2 * tpow(dy, 2)
g1 = metric.Metric(twoform=form)  # Note: don't have to specify coords since implied by basis of one-forms
```

Notice that the Metric class will represent itself as a twoform

```python
g1
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" title="\large a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y" /></a>
<!-- $a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$ -->

Now let's create the same metric from a matrix. We create the matrix elements first:

```python
matrix = Array([[a ** 2, 0], [0, b ** 2]])
matrix
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\left[\begin{matrix}a^{2}&space;&&space;0\\0&space;&&space;b^{2}\end{matrix}\right]" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\left[\begin{matrix}a^{2}&space;&&space;0\\0&space;&&space;b^{2}\end{matrix}\right]" title="\left[\begin{matrix}a^{2} & 0\\0 & b^{2}\end{matrix}\right]" /></a>
<!-- $\left[\begin{matrix}a^{2} & 0\\0 & b^{2}\end{matrix}\right]$ -->

Now we create the metric by specifying both the matrix *and* the coordinate system (since the axes of the Matrix 
are not labeled).

```python
g2 = metric.Metric(matrix=matrix, coord_system=cs)
```

Note that the Metric class automatically computes the two-form and uses it for representation:

```python
g2
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;a^{2}&space;\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;b^{2}&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y" title="\large a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y" /></a>
<!-- $a^{2} \operatorname{d}x \otimes \operatorname{d}x + b^{2} \operatorname{d}y \otimes \operatorname{d}y$ -->

Metrics can be inverted, and produce other metrics:

```python
g3 = g2.inverse
g3
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\frac{\operatorname{d}y&space;\otimes&space;\operatorname{d}y}{b^{2}}&space;&plus;&space;\frac{\operatorname{d}x&space;\otimes&space;\operatorname{d}x}{a^{2}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\frac{\operatorname{d}y&space;\otimes&space;\operatorname{d}y}{b^{2}}&space;&plus;&space;\frac{\operatorname{d}x&space;\otimes&space;\operatorname{d}x}{a^{2}}" title="\large \frac{\operatorname{d}y \otimes \operatorname{d}y}{b^{2}} + \frac{\operatorname{d}x \otimes \operatorname{d}x}{a^{2}}" /></a>
<!-- $\frac{\operatorname{d}y \otimes \operatorname{d}y}{b^{2}} + \frac{\operatorname{d}x \otimes \operatorname{d}x}{a^{2}}$ -->

## Curvature

It is easy to compute common curvature terms with `pystein`, such as Christoffel, Ricci, and Riemann tensor 
components. 

```python
from sympy import Function
from pystein import curvature
```

As an example, we create a metric with some curvature:

```python
x, y = cs.base_symbols()  # grab the coordinate parameters
F = Function('F')(x, y)  # Define an arbitrary function that depends on x and y
g4 = metric.Metric(twoform=F ** 2 * tpow(dx, 2) + b ** 2 * tpow(dy, 2))
```

Specific components may be computed individually, where the index numbers correspond to the same order as in 
the `CoordSystem` object.

```python
curvature.ricci_tensor_component(0, 0, g4).doit()
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;-&space;\frac{F{\left(x,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;y^{2}}&space;F{\left(x,y&space;\right)}}{b^{2}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;-&space;\frac{F{\left(x,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;y^{2}}&space;F{\left(x,y&space;\right)}}{b^{2}}" title="\large - \frac{F{\left(x,y \right)} \frac{\partial^{2}}{\partial y^{2}} F{\left(x,y \right)}}{b^{2}}" /></a>
<!-- $- \frac{F{\left(x,y \right)} \frac{\partial^{2}}{\partial y^{2}} F{\left(x,y \right)}}{b^{2}}$ -->

Often, it is desirable to compute all non-trivial components of a curvature tensor, which can also be done 
with the utility function `curvature.compute_components`, which will return the non trivial Christoffel, 
Ricci, and Riemann components:

```python
christoffels, riemanns, riccis = curvature.compute_components(metric=g4)
```

If in a Jupyter environment, these symbols can be concatenated and displayed as a single LaTeX formula using
the `display_components` utility.


## Matter

The `pystein.matter` module has some utilities for computing stress energy tensor components for common
matter sources.

```python
from pystein import matter
```

For example, a perfect fluid in 1D. Need to quickly redefine the coordinates to have a temporal coordinate, 
and we'll create a sample metric:

```python
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

Now use the matter module to create the stress energy tensor for perfect fluid

```python
T = matter.perfect_fluid(g5)
T
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;\left[\begin{matrix}\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p&space;&&space;0&space;&&space;0\\0&space;&&space;b^{2}&space;p&space;&&space;0\\0&space;&&space;0&space;&&space;p&space;S^{2}{\left(t,x&space;\right)}\end{matrix}\right]" title="\large \displaystyle \left[\begin{matrix}\rho - p Q^{2}{\left(t,y \right)} + p & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]" /></a>
<!-- $\displaystyle \left[\begin{matrix}\rho - p Q^{2}{\left(t,y \right)} + p & 0 & 0\\0 & b^{2} p & 0\\0 & 0 & p S^{2}{\left(t,x \right)}\end{matrix}\right]$ -->

Individual components may also be computed:

```python
utilities.clean_expr(curvature.einstein_tensor_component(0, 0, g5))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->

Note that in the limit Q -> 1: 

```python
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

It is also possible to directly compute the Einstein Equations:

```python
from pystein import gravity

utilities.clean_expr(gravity.einstein_equation(0, 0, g5, T))
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;8&space;\pi&space;\left(\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p\right)&space;=&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;8&space;\pi&space;\left(\rho&space;-&space;p&space;Q^{2}{\left(t,y&space;\right)}&space;&plus;&space;p\right)&space;=&space;-&space;\frac{Q^{2}{\left(t,y&space;\right)}&space;\frac{\partial^{2}}{\partial&space;x^{2}}&space;S{\left(t,x&space;\right)}}{b^{2}&space;S{\left(t,x&space;\right)}}" title="\large \displaystyle 8 \pi \left(\rho - p Q^{2}{\left(t,y \right)} + p\right) = - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}" /></a>
<!-- $\displaystyle 8 \pi \left(\rho - p Q^{2}{\left(t,y \right)} + p\right) = - \frac{Q^{2}{\left(t,y \right)} \frac{\partial^{2}}{\partial x^{2}} S{\left(t,x \right)}}{b^{2} S{\left(t,x \right)}}$ -->


[^1]: The default sympy.diffgeom behavior is to pass around coordinate functions, 
    which the sympy differentiation doesn't recognize as a *parameter* to other functions. We pass the symbols
    directly to allow normal differentiation to work.