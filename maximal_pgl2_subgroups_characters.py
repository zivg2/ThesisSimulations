from representations.characters.pgl2.pgl2_characters import PGL2StandardCharacter, \
    PGL2CuspidalCharacter, PGL2DiagonalizableCharacter, PGL2SignCharacter
from representations.characters.product_character import ProductCharacter
from representations.characters.field_character import FieldCharacter
from fields import SquareExtensionField
from representations.characters.pgl2.pgl2_characters import get_pgl2q_characters
from projective_sets.pgl2_maximal_subgroups import get_maximal_subgroups_up_to_conjugation
from utilities.primes import *
from projective_sets.pgl2 import PGL2
from group_actions import PGLGroupAction


for q in odd_primes_up_to(200):
    if q == 3:
        continue
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)

    square_field = SquareExtensionField.from_base_field(pgl2.get_field())

    characters = [PGL2StandardCharacter(q), PGL2CuspidalCharacter(q, FieldCharacter(square_field, 1, q-1))]
    primes = [x for x in odd_primes_up_to(q-2) if (q-1) % x == 0]
    subgroups = get_maximal_subgroups_up_to_conjugation(q)
    subgroups = subgroups[:-1]

    print(q)
    for subgroup in subgroups:
        good_characters = []
        for character in characters:
            character_result = sum([character.apply(x) for x in subgroup.get_all_elements()])
            character_result = round(character_result, 2)
            if character_result != 0:
                good_characters.append(character)
        print(subgroup, good_characters)
