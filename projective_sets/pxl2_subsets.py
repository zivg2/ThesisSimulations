from projective_sets.pgl import PGL, PGLElement
from fields import FieldFromInteger, SquareExtensionField
from .pgl2_maximal_subgroups import *


def psl2_a4_copies(field):
    q = field.size()
    result = []
    for a in field.get_all_elements():
        group = set(pgl2_a4(q, a))
        if not group:
            continue

        good_group = True
        for t in group:
            if t.det().legendre() != 1:
                good_group = False

        unique_group = True
        for copy in result:
            if group == copy:
                unique_group = False
                break

        if good_group and unique_group:
            result.append(group)

    return result

def pgl2_a4(q, a):
    if q % 3 == 0:
        return pgl2_a4_0(q, a)
    if q % 3 == 1:
        return pgl2_a4_1(q, a)
    else:
        return pgl2_a4_2(q, a)


def pgl2_a4_0(q, a):
    '''
    q is assumed to be 3 ** k
    '''
    pgl2 = PGL(2, q)
    field = pgl2.get_field()
    identity = pgl2.identity()

    s2_1 = pgl2.create([[a, -a*a-field.one()], [field.one(), -a]])
    s3 = pgl2.create([[field.one(), field.one()], [field.zero(), field.one()]])

    s2_2 = s3 * s2_1 * s3.inverse()
    s2_3 = s2_1 * s2_2

    elements = [identity, s2_1, s2_2, s2_3]
    elements_addition = [x*s3 for x in elements]
    elements_addition += [x * s3*s3 for x in elements]
    elements += elements_addition
    return elements


def pgl2_a4_1(q, a):
    '''
    q is assumed to be 1 mod 6
    '''
    pgl2 = PGL(2, q)
    field = pgl2.get_field()
    identity = pgl2.identity()
    unity_3_roots = [x for x in field.get_all_elements() if x * x + x + field.one() == field.zero()]
    zeta = unity_3_roots[0]
    field_two = field.one() + field.one()

    s2_1 = pgl2.create([[a, field.one()], [field_two*a*a, -a]])
    if s2_1.det() == field.zero():
        return []
    s3 = pgl2.create([[zeta, field.zero()], [field.zero(), field.one()]])

    s2_2 = s3 * s2_1 * s3.inverse()
    s2_3 = s2_1 * s2_2

    elements = [identity, s2_1, s2_2, s2_3]
    elements_addition = [x*s3 for x in elements]
    elements_addition += [x * s3*s3 for x in elements]
    elements += elements_addition
    return elements


def pgl2_a4_2(q, a):
    '''
    q is assumed to be 5 mod 6
    '''
    pgl2 = PGL(2, q)
    field = pgl2.get_field()
    identity = pgl2.identity()
    two = field.one() + field.one()
    three = two + field.one()
    nonsquare = SquareExtensionField.get_non_square_element(field)
    nonsquare_3_roots = [x for x in field.get_all_elements() if three * x * x == -nonsquare]
    x = nonsquare_3_roots[0]

    bs = [b for b in field.get_all_elements() if
          b*b-two*b*x*x+three*three*x*x*x*x+two*two*a*a*x*x == field.zero()]

    if len(bs) == 0:
        return []
    s2_1 = pgl2.create([[a, bs[0]], [field.one(), -a]])
    s3 = pgl2.create([[x, -three*x*x], [field.one(), x]])

    s2_2 = s3 * s2_1 * s3.inverse()
    s2_3 = s2_1 * s2_2

    elements = [identity, s2_1, s2_2, s2_3]
    elements_addition = [x*s3 for x in elements]
    elements_addition += [x*s3*s3 for x in elements]
    elements += elements_addition
    return elements


def psl2_a4(p):
    '''
    Legacy(?)
    p is assumed to be 1 mod 3
    '''
    psl2 = PSL2(p)
    field = psl2.get_field()
    identity = psl2.identity()
    unity_3_roots = [x for x in field.get_all_elements() if x * x + x + field.one() == field.zero()]
    a = unity_3_roots[0]
    field_two = field.one() + field.one()
    field_three = field.one() + field_two
    t = (field_two * a + field.one()) / field_three
    b = field.one()
    s1 = psl2.create([[t, b], [-field_two / (field_three * b), -t]])
    s2 = psl2.create([[a, field.zero()], [field.zero(), a*a]])

    elements = [identity, s1, s2, s2*s2, s1*s2*s1*s2*s2, s2*s1*s2*s2, s1*s2, s1*s2*s2,
                s2*s2*s1, s2*s1, s2*s1*s2, s2*s2*s1*s2*s2]
    return elements


def psl2_dihedral_imaginary_stabilizer(q) -> Iterable[PGL2Element]:
    elements = pgl2_dihedral_imaginary_stabilizer(q)
    elements = [x for x in elements if PSL2.is_determinant_square(x)]
    return elements


def pgl2_lower_triangular(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    elements = [pgl2.create([[a, field.zero()], [c, field.one()]])
                for a, c in product(field_elements, repeat=2) if a != field.zero()]
    return elements


def pgl2_lower_unipotent(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    elements = [pgl2.create([[field.one(), field.zero()], [c, field.one()]])
                for c in field_elements]
    return elements


def pgl2_diagonal(q) -> Iterable[PGL2Element]:
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_elements = field.get_all_elements()
    elements = [pgl2.create([[a, field.zero()], [field.zero(), field.one()]]) for a in field_elements if a != field.zero()]
    return elements


def pxl2_lubotzky_prime_based_subset(q, p):
    assert(q % 4 == 1)
    assert(p % 4 == 1)
    assert(p != q)
    field = FieldFromInteger.from_q(q)
    pgl2 = PGL2(q)
    max_p_sqrt = int(p**0.5)+1
    a_s = [(a, b, c, d) for a, (b, c, d) in product(range(1, max_p_sqrt, 2),
                                                    product(range(0, max_p_sqrt, 2), repeat=3))
           if a*a+b*b+c*c+d*d == p]
    a_s += [(a, -b, c, d) for a, b, c, d in a_s]
    a_s += [(a, b, -c, d) for a, b, c, d in a_s]
    a_s += [(a, b, c, -d) for a, b, c, d in a_s]
    a_s = set(a_s)
    a_s = [(field.create_element(a), field.create_element(b), field.create_element(c), field.create_element(d))
           for a, b, c, d in a_s]
    i = (-field.one()).sqrt()
    matrices = [pgl2.create([[a+i*b, c+i*d], [-c+i*d, a-i*b]]) for a, b, c, d in a_s]
    return matrices
