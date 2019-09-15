import numpy as np
from scipy.linalg import sqrtm
from typing import Tuple
from . import Representation
from .characters import Character
from .characters.special_representation_character import SpecialRepresentationCharacter
from utilities.general_utilities import measure, memorize


class UnitaryRepresentation(Representation):
    def __init__(self, representation: Representation, elements=None):
        self._representation = representation
        self._elements = elements
        result = self._calculate_conjugation_constants()
        self._conjugation_constant = result[0]
        self._conjugation_inverse = result[1]

    def _calculate_conjugation_constants(self) -> Tuple[np.ndarray, np.ndarray]:
        if self._elements is None:
            raise AssertionError()
        values = [self._representation.apply(element) for element in self._elements]
        symmetric_values = [np.matmul(x.transpose(), x) for x in values]
        conjugation_constant_square = np.average(symmetric_values, 0)
        conjugation_constant = np.real(sqrtm(conjugation_constant_square))
        conjugation_inverse = np.linalg.inv(conjugation_constant)
        return conjugation_constant, conjugation_inverse

    @measure
    def apply(self, x) -> np.ndarray:
        non_conjugated_value = self._representation.apply(x)

        temp = self._conjugation_constant
        temp = np.matmul(temp, non_conjugated_value)
        temp = np.matmul(temp, self._conjugation_inverse)
        return temp

    def apply_up_to_conjugation(self, x) -> np.ndarray:
        return self._representation.apply_up_to_conjugation(x)

    def get_character(self) -> Character:
        return SpecialRepresentationCharacter(self, self.apply_up_to_conjugation)

    def dim(self) -> int:
        return self._representation.dim()

    def __str__(self):
        return 'u_' + str(self._representation)
