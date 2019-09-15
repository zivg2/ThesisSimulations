from . import Representation
from .characters.product_character import ProductCharacter, Character
from utilities.general_utilities import *
from itertools import product
import numpy as np


class TensorRepresentation(Representation):
    def __init__(self, representation1: Representation, representation2: Representation):
        self._representation1 = representation1
        self._representation2 = representation2
        self._basis_indices = list(product(range(representation1.dim()), range(representation2.dim())))

    @measure
    def apply(self, g) -> np.ndarray:
        result = []
        base_call1 = self._representation1.apply(g)
        base_call2 = self._representation2.apply(g)
        for indices in self._basis_indices:
            i1 = indices[0]
            i2 = indices[1]
            vector1 = base_call1[i1, :]
            vector2 = base_call2[i2, :]
            result_vector = self._tensor_vectors(vector1, vector2)
            result.append(result_vector)

        return np.asarray(result)

    @staticmethod
    def _tensor_vectors(vector1: np.ndarray, vector2: np.ndarray) -> np.ndarray:
        result = np.matmul(vector1[:, None], vector2[None, :])
        result = result.flatten('C')
        return result

    def get_character(self) -> Character:
        return ProductCharacter(self._representation1.get_character(), self._representation2.get_character())

    def dim(self) -> int:
        return self._representation1.dim() * self._representation2.dim()

    def __str__(self):
        return 'tensor(%s, %s)' % (str(self._representation1), str(self._representation2))



