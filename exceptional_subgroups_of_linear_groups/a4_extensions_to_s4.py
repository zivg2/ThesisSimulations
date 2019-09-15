from utilities.q_group_from_file import get_q_groups_from_file
from group_actions.group_utiliies import get_extension_of_order_2
from projective_sets.pgl import PGL


a4_copies = get_q_groups_from_file(r'results/a4_in_low_psl2q_up_to_conjugation.txt')
good_groups = {}

for q in a4_copies:
    good_groups[q] = []
    pgl = PGL(2, q)
    if q % 8 in [3, 5]:
        good_groups[q] = a4_copies[q]
    else:
        for copy in a4_copies[q]:
            s4 = get_extension_of_order_2(copy, pgl, lambda x: x.det().legendre() == 1)
            good_groups[q].append(s4)
    for x in good_groups[q]:
        print(q, x)

