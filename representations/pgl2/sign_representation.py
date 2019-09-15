from representations import Representation
from representations.characters.pgl2.pgl2_sign_character import PGL2SignCharacter, Character
from projective_sets.pgl2_element import PGL2Element
import numpy as np


class SignRepresentation(Representation):
    def apply(self, x: PGL2Element) -> np.ndarray:
        det = x.det()
        sign = det.legendre()
        return sign * np.ones((1, 1))

    def dim(self) -> int:
        return 1

    def get_character(self) -> Character:
        return PGL2SignCharacter()

    def __str__(self):
        return 'sgn'
