# Tutorial: Numerical Geodesics

This tutorial demonstrates in brief how to use the numeric tools in `pystein`. For other tutorials 
see [all tutorials](tutorials.md).

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
<br>






