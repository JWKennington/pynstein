# Collapsing Cosmology Research Utilities
[![PyPI version](https://img.shields.io/pypi/v/collapse)](https://pypi.org/project/collapse/)
[![PyPI downloads](https://img.shields.io/pypi/dm/collapse)](https://pypi.org/project/collapse/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/collapse)](https://pypi.org/project/collapse/)
[![Build](https://img.shields.io/travis/JWKennington/collapse)](https://pypi.org/project/collapse/)
[![codecov](https://codecov.io/gh/JWKennington/collapse/branch/master/graph/badge.svg?token=G418VYV5LR)](undefined)
[![CodeFactor Quality](https://img.shields.io/codefactor/grade/github/JWKennington/collapse?&label=codefactor)](https://pypi.org/project/collapse/)
[![License](https://img.shields.io/github/license/JWKennington/collapse?color=magenta&label=License)](https://pypi.org/project/collapse/)



The `collapse` package contains utilities for computing symbolic and numerical expressions related to the time evolution
of collapsing cosmologies. 


## Symbolic Tools
The `collapse` package makes use of `sympy` to compute symbolic curvature equations (EFE).
[Specific Details](./collapse/symbolic/README.md)

### Example Computation: FLRW Cosmology

```python
# Load the predefined FLRW metric
from collapse.symbolic import metric, gravity, utilities
flrw = metric.flrw().subs({'c': 1})
flrw
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\large&space;\displaystyle&space;-&space;c^{2}&space;\operatorname{d}t&space;\otimes&space;\operatorname{d}t&space;&plus;&space;a^{2}{\left(t&space;\right)}&space;\left(\operatorname{d}x&space;\otimes&space;\operatorname{d}x&space;&plus;&space;\operatorname{d}y&space;\otimes&space;\operatorname{d}y&space;&plus;&space;\operatorname{d}z&space;\otimes&space;\operatorname{d}z\right)" title="\large \displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)" /></a>
<!-- $\displaystyle - c^{2} \operatorname{d}t \otimes \operatorname{d}t + a^{2}{\left(t \right)} \left(\operatorname{d}x \otimes \operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}y + \operatorname{d}z \otimes \operatorname{d}z\right)$ -->


```python
efe_00 = utilities.clean_expr(gravity.einstein_equation(0, 0, flrw))
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

