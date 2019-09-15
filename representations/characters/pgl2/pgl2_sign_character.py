from representations.characters.character import Character
from projective_sets.pgl2_element import PGL2Element


class PGL2SignCharacter(Character):
    def apply(self, x: PGL2Element) -> float:
        return x.det().legendre()

    def __str__(self):
        return 'χ_sgn'
