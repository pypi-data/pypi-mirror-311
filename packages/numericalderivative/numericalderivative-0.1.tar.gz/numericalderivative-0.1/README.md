# numericalderivative

## What is it?

The goal of this project is to compute the first derivative of a function
using finite difference formulas.
The difficulty with these formulas is that it must use a finite difference 
step which must be neither too large (otherwise truncation error dominates 
the error) nor too small (otherwise condition error dominates).
To solve this issue, the module provides algorithms to compute an approximate
optimal finite difference step.

Furthermore, this package provides benchmark problems for numerical
differentiation.

This module allows you to do this:

```python
import math
import numericalderivative as nd

def scaled_exp(x):
    alpha = 1.0e6
    return math.exp(-x / alpha)


h0 = 1.0e5
x = 1.0e0
algorithm = nd.SteplemanWinarsky(scaled_exp, x)
h_optimal, iterations = algorithm.compute_step(h0)
number_of_function_evaluations = algorithm.get_number_of_function_evaluations()
f_prime_approx = algorithm.compute_first_derivative(h_optimal)
```

## Authors

* Michaël Baudin, 2024

## Installation

To install from Github:

```bash
git clone https://github.com/mbaudin47/numerical_derivative.git
cd numerical_derivative
python setup.py install
```

## References
- Gill, P. E., Murray, W., Saunders, M. A., & Wright, M. H. (1983). 
  Computing forward-difference intervals for numerical optimization. 
  SIAM Journal on Scientific and Statistical Computing, 4(2), 310-321.
- Adaptive numerical differentiation
  R. S. Stepleman and N. D. Winarsky
  Journal: Math. Comp. 33 (1979), 1257-1264 
- Dumontet, J., & Vignes, J. (1977). 
  Détermination du pas optimal dans le calcul des dérivées sur ordinateur. 
  RAIRO. Analyse numérique, 11 (1), 13-25.

## Roadmap
- Use bracket_step as a list of two floats in GillMurraySaundersWright
  and DumontetVignes (this is done in SteplemanWinarsky)
- Create a benchmark feature to test a given method on several 
  benchmark problems
- Use a relative precision in SteplemanWinarsky and GillMurraySaundersWright.
- Remove NumericalDerivative: move it to FiniteDifferenceFormula.

