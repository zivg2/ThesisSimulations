from .sign_character import SignCharacter, Character
from .sn_table_character import SNTableCharacter, Partition
from .standard_character import StandardCharacter
from representations.characters.trivial_character import TrivialCharacter
from representations.characters.product_character import ProductCharacter
from typing import List


def get_s5_nontrivial_characters() -> List[Character]:
    sign_character = SignCharacter()
    standard_character = StandardCharacter()
    chi5 = SNTableCharacter({
                                Partition([1, 1, 1, 1, 1]): 5,
                                Partition([2, 1, 1, 1]): 1,
                                Partition([2, 2, 1]): 1,
                                Partition([3, 1, 1]): -1,
                                Partition([3, 2]): 1,
                                Partition([4, 1]): -1,
                                Partition([5]): 0,
                            },
                            "χ5")

    chi6 = SNTableCharacter({
                                Partition([1, 1, 1, 1, 1]): 6,
                                Partition([2, 1, 1, 1]): 0,
                                Partition([2, 2, 1]): -2,
                                Partition([3, 1, 1]): 0,
                                Partition([3, 2]): 0,
                                Partition([4, 1]): 0,
                                Partition([5]): 1,
                            },
                            "χ6")

    return [sign_character, standard_character, ProductCharacter(sign_character, standard_character),
            chi5, ProductCharacter(sign_character, chi5), chi6]

def get_s5_characters():
    nontrivial_characters = get_s5_nontrivial_characters()
    trivial_character = TrivialCharacter()
    return [trivial_character] + nontrivial_characters
