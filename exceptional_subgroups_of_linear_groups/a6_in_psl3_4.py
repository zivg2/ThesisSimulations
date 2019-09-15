from group_actions import PGLGroupAction
from projective_sets.pgl import PGL
from itertools import product
from fields import SquareExtensionField


def a6_in_psl3_4(pgl):
    field = pgl.get_field()
    one = field.one()
    zero = field.zero()
    assert(isinstance(field, SquareExtensionField))
    extension_element = field.extension_element()

    e1 = pgl.create([
            [one, zero, one],
            [zero, one, zero],
            [zero, zero, one]
        ])

    e2 = pgl.create([
            [one, zero, zero],
            [zero, one, one],
            [zero, zero, one]
        ])

    e3 = pgl.create([
            [one, zero, zero],
            [zero, one, zero],
            [extension_element, one, one]
        ])

    e4 = pgl.create([
            [one, zero, zero],
            [one, one, zero],
            [zero, zero, one]
        ])

    members = {pgl.identity()}
    for k in range(8):
        for x in product([e1, e2, e3, e4], members):
            res = x[0] * x[1]
            members.add(res)
            if len(members) == 360:
                break
    return members


pgl = PGL(3, 4)
action = PGLGroupAction(pgl)
members = a6_in_psl3_4(pgl)
vector_space = action.get_acted_upon_elements()
orbit_elements = [action.apply(g, vector_space[0]) for g in members]
orbit = list(set(orbit_elements))
print(len(orbit))
