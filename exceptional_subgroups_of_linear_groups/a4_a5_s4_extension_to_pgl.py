from utilities.q_group_from_file import get_q_groups_from_file
from group_actions.group_utiliies import get_extension_of_order_2
from projective_sets.pgl import PGL


group_copies = get_q_groups_from_file(r'results/groups_in_low_psl2q_up_to_conjugation.txt')
good_groups = {}


for q in group_copies:
    good_groups[q] = []
    pgl = PGL(2, q)
    for copy in group_copies[q]:
        extension = get_extension_of_order_2(copy, pgl, lambda x: x.det().legendre() == -1)
        good_groups[q].append(extension)
    for x in good_groups[q]:
        print(q, x)

