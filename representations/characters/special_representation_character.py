from .representation_character import RepresentationCharacter
from representations.representation import Representation

import numpy as np


class SpecialRepresentationCharacter(RepresentationCharacter):
    def __init__(self, representation: Representation, special_apply_function):
        super().__init__(representation)
        self._special_apply_function = special_apply_function

    def apply(self, x) -> float:
        result = float(np.trace(self._special_apply_function(x)))
        return result
