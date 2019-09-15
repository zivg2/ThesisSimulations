from typing import Iterable
from fields import SquareExtensionField
from projective_sets.pgl2 import PGL2, PGL2Element
from projective_sets.psl2 import PSL2
from elements_generator import ElementsGenerator, IterableElementsGenerator
from itertools import product
from utilities.primes import *


def pgl2_dihedral_imaginary_stabilizer(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    non_square = SquareExtensionField.get_non_square_element(field)
    field_elements = field.get_all_elements()
    elements = [pgl2.create2(field.one(), b, b*non_square, field.one()) for b in field_elements if b != field.zero()]
    elements.append(pgl2.create2(field.zero(), field.one(), non_square, field.zero()))
    elements.extend([pgl2.create2(field.one(), b, -b*non_square, -field.one()) for b in field_elements])
    elements.append(pgl2.create2(field.zero(), field.one(), -non_square, field.zero()))
    elements.append(pgl2.identity())
    return elements


def pgl2_upper_triangular(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    elements = [pgl2.create2(a, b, field.zero(), field.one())
                for a, b in product(field_elements, repeat=2) if a != field.zero()]
    return elements


def pgl2_zero_infinity_stabilizer(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    elements = [pgl2.create2(a, field.zero(), field.zero(), field.one())
                for a in field_elements if a != field.zero()]
    elements += [pgl2.create2(field.zero(), a, field.one(), field.zero())
                 for a in field_elements if a != field.zero()]
    return elements


def pgl2_s4(q) -> Iterable[PGL2Element]:
    assert(q % 8 == 3 or q % 8 == 5)
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    r = pgl2.create2(field.zero(), field.one(), -field.one(), field.one())
    if q % 8 == 3:
        minus_two = -field.one()-field.one()
        a = minus_two.sqrt()
        s = pgl2.create2(field.one(), minus_two, field.one() + a, -field.one())
    else:
        minus_one = -field.one()
        i = minus_one.sqrt()
        s = pgl2.create2(field.zero(), i, field.one(), field.zero())
    elements = [pgl2.identity(), r, r*r, r*s, r*r*s, r*s*r, r*s*r*r,
                r*r*s*r, r*r*s*r*r, r*s*r*r*s, r*r*s*r*s, r*r*s*r*r*s, r*s*r*r*s*r]
    elements += [s, s*r, s*r*r, s*r*s, s*r*r*s, s*r*s*r*r,
                 s*r*r*s*r, s*r*r*s*r*r, s*r*s*r*r*s, s*r*r*s*r*s, s*r*s*r*r*s*r]

    return elements


def get_maximal_subgroups_up_to_conjugation(q) -> Iterable[ElementsGenerator[PGL2Element]]:
    p, k = get_prime_base_and_exponent(q)
    pgl2 = PGL2(q)
    prime_powers_inverses = []
    if k % 2 == 0:
        prime_powers_inverses += [k // 2]
    prime_powers_inverses += [k//i for i in odd_primes_up_to(k) if k % i == 0]
    subgroups = [IterableElementsGenerator(pgl2_zero_infinity_stabilizer(q), "Stab(0, ∞)"),
                 IterableElementsGenerator(pgl2_dihedral_imaginary_stabilizer(q), "Stab(𝛿, -𝛿)"),
                 IterableElementsGenerator(pgl2_upper_triangular(q), "Stab(0)"),
                 ]
    subgroups += [pgl2.smaller_pgl2(p ** i) for i in prime_powers_inverses]
    if q > 3 and k == 1 and q % 8 == 3 or q % 8 == 5:
        subgroups.append(IterableElementsGenerator(pgl2_s4(q), "S4"))
    subgroups += [PSL2(q)]
    return subgroups
