from symmetric_group.s5_maximal_subgroups import s5_maximal_subgroups
from symmetric_group.characters.s5_characters import get_s5_nontrivial_characters

for group in s5_maximal_subgroups():
    good_characters = []
    for character in get_s5_nontrivial_characters():
        value = sum(character.apply(x) for x in group.get_all_elements())
        if value > 0:
            good_characters.append(character)
    print(group)
    print(good_characters)
    print()
