from numpy import exp, pi, arange
import numpy as np
from sympy.ntheory import totient
from utilities.primes import odd_primes_up_to


def divisors_over_one(n):
    large_divisors = [n]
    for i in range(2, int(np.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n // i)
    for divisor in reversed(large_divisors):
        yield divisor


def nth_unity_roots(n):
    return exp(2j * pi / n * arange(n))


def nth_unity_roots_not_one(n):
    return exp(2j * pi / n * arange(1, n))


def two_edge_mini_polynomial_for_unity_root(zeta):
    val = np.real(zeta + np.conjugate(zeta))
    return np.polynomial.Polynomial([-2-val, 0, 1])


def k3_mini_polynomial_for_unity_root(zeta):
    val = np.real(zeta + np.conjugate(zeta))
    return np.polynomial.Polynomial([-val, -3, 0, 1])


def loop_mini_polynomial_for_unity_root(zeta):
    val = np.real(zeta + np.conjugate(zeta))
    return np.polynomial.Polynomial([-val, 1])


def polynomial_product(generator, values):
    res = np.polynomial.Polynomial([1])
    for value in values:
        res *= generator(value)
    return res


def average_matching_polynomial(q, polynomial_generator):
    p1 = polynomial_generator(1)
    q_plus_one_polys = [q*(q-1)//2 * totient(d) * p1 ** ((q+1) // d - 1) *
                        (polynomial_product(polynomial_generator, nth_unity_roots_not_one(d))) ** ((q+1) // d)
                        for d in divisors_over_one(q+1)]
    q_minus_one_polys = [q*(q+1)//2 * totient(d) * p1 *
                         (polynomial_product(polynomial_generator, nth_unity_roots(d))) ** ((q-1) // d)
                         for d in divisors_over_one(q-1)]
    res = p1 ** q + \
        (q*q-1)*polynomial_product(polynomial_generator, nth_unity_roots(q)) + \
        sum(q_plus_one_polys) + sum(q_minus_one_polys)
    return res / (q**3 - q)


qs = odd_primes_up_to(100)

for q in qs:
    p = average_matching_polynomial(q, loop_mini_polynomial_for_unity_root)
    roots = p.roots()
    roots_abs = np.abs(roots)
    real_roots = [x for x in roots if np.imag(x) == 0]
    print(real_roots)
    print()
