from representations import Representation
import numpy as np
from typing import Iterable


class RepresentationAdjacencyMatrix:
    def __init__(self, representation: Representation):
        self._representation = representation

    def get_matrix(self, generators: Iterable) -> np.ndarray:
        representation_values = [self._representation.apply(x) for x in generators]
        return sum(representation_values)

    def get_matrix_up_to_conjugation(self, generators: Iterable) -> np.ndarray:
        representation_values = [self._representation.apply_up_to_conjugation(x) for x in generators]
        return sum(representation_values)
