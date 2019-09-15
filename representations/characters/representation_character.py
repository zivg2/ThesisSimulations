from representations.characters import Character
from representations import Representation

import numpy as np


class RepresentationCharacter(Character):
    def __init__(self, representation: Representation):
        self._representation = representation

    def apply(self, x) -> float:
        result = np.trace(self._representation.apply_up_to_conjugation(x), dtype=complex)
        return result

    def __str__(self):
        return 'χ(%s)' % str(self._representation)
