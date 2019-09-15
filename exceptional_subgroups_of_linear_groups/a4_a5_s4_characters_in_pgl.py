from utilities.q_group_from_file import get_q_groups_from_file
from representations.characters.pgl2.pgl2_characters import get_pgl2q_characters


q_to_group_copies = get_q_groups_from_file(r'results/groups_in_low_pgl2q_up_to_conjugation.txt')
for q in q_to_group_copies:
    group_copies = q_to_group_copies[q]
    characters = get_pgl2q_characters(q)[1:]
    for copy in group_copies:
        print(q, len(copy))
        for character in characters:
            value = sum(character.apply(x) for x in copy)
            value = round(value) / len(copy)
            print(character, value)
        print()
