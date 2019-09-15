from projective_sets.pgl import PGL
from group_actions import PGLGroupAction
from utilities.generating_sets import generators_of_a5

q = 11
pgl = PGL(2, q)
action = PGLGroupAction(pgl)
field = pgl.get_pf().get_field()

zetas = [x for x in field.get_all_elements() if
         (x ** 5 == field.one() and x != field.one())]

groups = set()

for zeta in zetas:
    for sign in [field.one(), -field.one()]:
        alpha = sign / (zeta - zeta.inverse())
        for beta in field.get_all_elements():
            if beta == field.zero():
                continue
            gamma = (-field.one() - (alpha**2)) / beta
            v5 = pgl.create([[zeta, field.zero()], [field.zero(), zeta.inverse()]])
            v2 = pgl.create([[alpha, beta], [gamma, -alpha]])
            group = generators_of_a5(v5, v2, pgl.identity())
            add = True
            for group2 in groups:
                equal = True
                for x in group:
                    if x not in group2:
                        equal = False
                        break
                if equal:
                    add = False
                    break
            if add:
                groups.add(group)

for group in groups:
    print(q, set(group))
    zero = pgl.get_pf().zero()
    orbit0 = set([action.apply(g, zero) for g in group])
    print(len(orbit0), [int(x[0] / x[1]) if x[1] != field.zero() else 'inf' for x in orbit0])

    print()
