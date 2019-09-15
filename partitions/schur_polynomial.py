from sympy import symbols, Matrix, polys
from utilities.general_utilities import memorize


@memorize
def _xs(n):
    symbols_names = ','.join(['x%d' % i for i in range(n)])
    return symbols(symbols_names)


def _schur_alternating_polynomial(composition):
    n = len(composition)
    x = _xs(n)
    matrix = Matrix([[x[j] ** (composition[i] + n - i - 1) for j in range(n)] for i in range(n)])
    return matrix.det().as_poly()


@memorize
def _schur_denominator(n):
    return _schur_alternating_polynomial(tuple([0] * n))


def schur_polynomial(composition):
    n = len(composition)
    f = _schur_alternating_polynomial(composition)
    g = _schur_denominator(n)
    result = polys.polytools.div(f, g)
    return result[0]
