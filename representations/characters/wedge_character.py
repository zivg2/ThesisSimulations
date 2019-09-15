from .character import Character
from .trivial_character import TrivialCharacter
from .representation_character import RepresentationCharacter
from .. import Representation
import numpy as np
from utilities.general_utilities import memorize, measure


class WedgeCharacter(Character):
    def __init__(self, representation: Representation, power: int):
        self._representation = representation
        self._power = power
        self._lower_wedges = [WedgeCharacter.create_wedge_character(representation, i) for i in range(power)]

    @classmethod
    def create_wedge_character(cls, representation: Representation, power: int) -> Character:
        if power == 0:
            return TrivialCharacter()
        elif False and power == 1:
            return RepresentationCharacter(representation)
        else:
            return cls(representation, power)

    @measure
    def apply(self, x) -> float:
        summands = [(-1)**(k-1) * self._apply_power_representation(x, k) * self._lower_wedges[self._power - k].apply(x)
                    for k in range(1, self._power+1)]
        return 1/self._power * sum(summands)

    @measure
    @memorize
    def _apply_power_representation(self, x, k):
        return float(np.trace(np.linalg.matrix_power(self._representation.apply_up_to_conjugation(x), k)))

    def __str__(self):
        return 'χ_wedge(%s, %d)' % (str(self._representation), self._power)
