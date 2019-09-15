import numpy as np
from scipy.special import comb

from utilities.general_utilities import *
from utilities.wedge_maker import WedgeMaker
from . import Representation
from .trivial_representation import TrivialRepresentation
from .characters.wedge_character import WedgeCharacter, Character


class WedgeRepresentation(Representation):
    def __init__(self, base_representation: Representation, power: int):
        self._base_representation = base_representation
        self._power = power
        self._wedge_maker = WedgeMaker(self._power)
        self._basis_indices = list(combinations(range(base_representation.dim()), power))

    @classmethod
    def create(cls, base_representation: Representation, power: int) -> Representation:
        if power == 0:
            return TrivialRepresentation()
        elif power == 1:
            return base_representation
        else:
            return cls(base_representation, power)

    @measure
    def apply(self, x) -> np.ndarray:
        base_call = self._base_representation.apply(x)
        return self._wedge_maker.get_wedge_matrix(base_call)

    def get_character(self) -> Character:
        return WedgeCharacter.create_wedge_character(self._base_representation, self._power)

    def _base_dim(self):
        return self._base_representation.dim()

    def dim(self) -> int:
        return int(comb(self._base_dim(), self._power))

    def __str__(self):
        return 'wedge(%s, %d)' % (str(self._base_representation), self._power)



