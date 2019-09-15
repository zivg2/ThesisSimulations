from . import Representation
from .characters.sum_character import SumCharacter, Character
from utilities.general_utilities import *
import numpy as np
from typing import List


class SumRepresentation(Representation):
    def __init__(self, representation1: Representation, representation2: Representation):
        self._representation1 = representation1
        self._representation2 = representation2
        self._d1 = representation1.dim()
        self._d2 = representation2.dim()
        self.name = '(%s + %s)' % (str(self._representation1), str(self._representation2))

    @classmethod
    def from_list(cls, representation_list: List[Representation]) -> Representation:
        result = representation_list[0]
        first_representation = True
        for representation in representation_list:
            if first_representation:
                first_representation = False
                continue
            result = cls(result, representation)
        return result

    @measure
    def apply(self, g) -> np.ndarray:
        base_call1 = self._representation1.apply(g)
        base_call2 = self._representation2.apply(g)
        return np.block([[base_call1, np.zeros((self._d1, self._d2))], [np.zeros((self._d2, self._d1)), base_call2]])

    def get_character(self) -> Character:
        return SumCharacter(self._representation1.get_character(), self._representation2.get_character())

    def dim(self) -> int:
        return self._representation1.dim() + self._representation2.dim()

    def __str__(self):
        return self.name



