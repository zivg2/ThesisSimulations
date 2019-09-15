from .general_utilities import memorize
from math import log


def odd_primes_up_to(n):
    primes = []
    for i in range(3, n+1, 2):
        is_prime = True
        for p in primes:
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
            yield i


def primes_up_to(n):
    yield(2)
    for x in odd_primes_up_to(n):
        yield x


def prime_powers_up_to(basis, exponent):
    for prime in primes_up_to(basis):
        for k in range(1, exponent):
            yield prime ** k


def odd_prime_powers_up_to(basis, exponent):
    for prime in odd_primes_up_to(basis):
        for k in range(1, exponent):
            yield prime ** k


def odd_primes_between(m, n):
    for i in odd_primes_up_to(n):
        if i >= m:
            yield i


def odd_1_mod_4_primes_up_to(n):
    for i in odd_primes_up_to(n):
        if i % 4 == 1:
            yield i


def get_prime_base_and_exponent(q):
    # q is assumed to be a prime power
    p0 = q
    for p in range(2, int(q ** 0.5) + 2):
        if q % p == 0:
            p0 = p
    k = int(round(log(q, p0)))
    return p0, k