from projective_sets.pxl2_subsets import psl2_a4_copies
from group_actions import PGLGroupAction
from projective_sets.pgl import PGL

qs = [3, 5, 7, 11, 23, 31, 47]

for q in qs:
    pgl = PGL(2, q)
    action = PGLGroupAction(pgl)
    field = pgl.get_pf().get_field()
    a4_copies = psl2_a4_copies(field)
    good_a4 = [a4_copies[0]]
    a4_copies.pop(0)

    if q % 8 in [1, 7]:
        while len(a4_copies) > 0 or len(good_a4) < 2:
            a4 = a4_copies[0]
            unique_a4 = True
            for element in pgl.get_all_elements():
                if element.det().legendre() != 1:
                    continue
                a4_conjugated = set([element*x*element.inverse() for x in a4])
                if a4_conjugated in good_a4:
                    unique_a4 = False
                    break
            if unique_a4:
                good_a4.append(a4)
            a4_copies.pop(0)

    for copy in good_a4:
        print(q, copy)
