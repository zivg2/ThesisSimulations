from projective_sets.pgl2 import PGL2
from projective_sets.pgl import PGLElement
from typing import Iterable
from itertools import product


def pgl2_unipotent_conjugation_class(q) -> Iterable[PGLElement]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    results = [pgl2.create([[field.one(), x], [field.zero(), field.one()]])
               for x in field_elements if x != field.zero()]
    results += [pgl2.create([[field.one(), field.zero()], [x, field.one()]])
                for x in field_elements if x != field.zero()]
    results += [pgl2.create([[a, b], [-(a-field.one())*(a-field.one())/b, field.one() + field.one() - a]])
                for a, b in product(field_elements, repeat=2) if a != field.one() and b != field.zero()]
    return results


def pgl2_imaginary_roots_conjugation_class(q) -> Iterable[PGLElement]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    results = [pgl2.create([[field.one(), b],[c, -field.one()]])
               for b, c in product(field.get_all_elements(), repeat=2) if (field.one() + b*c).legendre() < 0]
    results += [pgl2.create([[field.zero(), b], [field.one(), field.zero()]])
                for b in field_elements if b.legendre() < 0]
    return results


def pgl2_diagonal_conjugation_class(q) -> Iterable[PGLElement]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    results = [pgl2.create([[field.one(), b],[c, -field.one()]])
               for b, c in product(field.get_all_elements(), repeat=2) if (field.one() + b*c).legendre() > 0]
    results += [pgl2.create([[field.zero(), b], [field.one(), field.zero()]])
                for b in field_elements if b.legendre() > 0]
    return results


def pgl2_conjugation_class(q, square_trace_to_det_ratio) -> Iterable[PGLElement]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    field_two = field.one() + field.one()
    field_four = field_two + field_two
    s = square_trace_to_det_ratio
    assert(s != field_four and s != field.zero())

    results = [pgl2.create([[field.zero(), field.one()], [-d*d/s, d]])
               for d in field_elements if d != field.zero()]
    results += [pgl2.create([[field.one(), b],
                             [-(d*d+(field_two - s)*d + field.one()) / (b*s), d]])
                for b, d in product(field_elements, repeat=2) if b != field.zero() and d != -field.one()]
    discriminant_square = s*s-field_four*s
    if discriminant_square.legendre() > 0:
        discriminant = discriminant_square.sqrt()
        ds = [(s - field_two + discriminant) / field_two, (s - field_two - discriminant) / field_two]
        results += [pgl2.create([[field.one(), field.zero()],
                                 [c, d]])
                    for c, d in product(field_elements, ds)]
    return results


