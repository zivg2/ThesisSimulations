from group_actions import FiniteGroupAction, PGLGroupAction, SNGroupAction
from projective_sets.pgl2 import PGL2
from projective_sets.psl2 import PSL2
from numpy import arange, pi, exp, average, flip
import numpy as np
from numpy.polynomial.polynomial import polyfromroots
from utilities.my_polynomial import MyPolynomial
from utilities.primes import odd_primes_up_to
from group_actions.group_utiliies import get_sn_conjugation_classes, get_partition_amount
from numpy.linalg import matrix_rank
from itertools import product
from scipy.spatial import Delaunay, ConvexHull
from sympy.ntheory import totient


def nth_unity_roots(n):
    return exp(2j * pi / n * arange(n))


def find_orbits(action: FiniteGroupAction, conjugation_classes):
    acting_elements = conjugation_classes.keys()
    lengths = {}
    for acting_element in acting_elements:
        cycle_lengths = tuple(get_cycle_lengths(action, acting_element))
        if cycle_lengths not in lengths:
            lengths[cycle_lengths] = 0
        lengths[cycle_lengths] += conjugation_classes[acting_element]
    return lengths


def get_cycle_lengths(action: FiniteGroupAction, acting_element):
    elements_used = []
    cycle_lengths = []
    for element in action.get_acted_upon_elements():
        first_element = element
        if element in elements_used:
            continue
        cycle_length = 0
        while cycle_length == 0 or element != first_element:
            cycle_length += 1
            elements_used.append(element)
            element = action.apply(acting_element, element)
        cycle_lengths.append(cycle_length)
    return sorted(cycle_lengths)


def get_cycle_roots(lengths):
    roots_lists = [nth_unity_roots(n) for n in lengths]
    roots = [item for sublist in roots_lists for item in sublist]
    return roots


def polynomials_inner_product(p1, p2, a, b):
    integrated = np.polyint(np.polymul(p1, p2))
    return np.polyval(integrated, b) - np.polyval(integrated, a)


def get_polynomials(orbit_to_amount_dictionary):
    cycle_roots = [get_cycle_roots(lengths) for lengths in orbit_to_amount_dictionary]
    new_eigenvalues = [[np.real(x + 1 / x) for x in y] for y in cycle_roots]
    new_polynomials = [np.round(polyfromroots(x)) for x in new_eigenvalues]
    return new_polynomials


def get_average_polynomial(orbit_to_amount_dictionary):
    new_polynomials = get_polynomials(orbit_to_amount_dictionary)
    return average(new_polynomials, 0, list(orbit_to_amount_dictionary.values()))


def get_action_average_polynomial(action, conjugation_classes):
    orbit_lengths = find_orbits(action, conjugation_classes)
    return get_average_polynomial(orbit_lengths)


def pop_if_found(dict, key):
    if key in dict:
        dict.pop(key)


qs = [11]

for q in qs:
    print('q = %d' % q)
    group = PGL2(q)
    action = PGLGroupAction(group)
    conjugation_classes = group.get_conjugation_classes()

    sn_average_polynomial = get_action_average_polynomial(SNGroupAction(q+1), get_sn_conjugation_classes(q+1))

    orbit_lengths = find_orbits(action, conjugation_classes)
    polynomials = get_polynomials(orbit_lengths)
    polynomials2 = np.asarray(polynomials)
    polynomials.append(sn_average_polynomial)
    polynomials3 = np.asarray(polynomials)
    r1 = matrix_rank(polynomials2)
    r2 = matrix_rank(polynomials3)
    poly_number = len(polynomials2)
    print(poly_number, r1, r2)
    print(orbit_lengths)
    print()
