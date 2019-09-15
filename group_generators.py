from utilities.q_group_from_file import get_q_groups_from_file
from itertools import combinations, product
from copy import copy



group_copies = get_q_groups_from_file(r'results/groups_in_low_pgl2q_up_to_conjugation.txt')
for q in group_copies:
    for group_copy in group_copies[q]:
        for (x, y) in combinations(group_copy, 2):
            generating_set = {x, y, x.inverse(), y.inverse()}
            generated_set = copy(generating_set)
            generated_set_last = set()
            while len(generated_set) > len(generated_set_last):
                generated_set_last = copy(generated_set)
                generated_set = generated_set.union([a*b for a, b in product(generated_set_last, generating_set)])

            if len(generated_set) == len(group_copy):
                print(q, x, y, generated_set)
                break
