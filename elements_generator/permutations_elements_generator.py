from .elements_generator import ElementsGenerator
from utilities.general_utilities import class_property_memorize
import numpy as np
from itertools import permutations


class PermutationsElementsGenerator(ElementsGenerator):
    def __init__(self, permuted_elements):
        self._permuted_elements = permuted_elements

    @class_property_memorize
    def get_all_elements(self):
        return list(permutations(self._permuted_elements))

    def random_element(self):
        return tuple(np.random.permutation(self._permuted_elements))

    def __str__(self):
        return "Perm(%d)" % len(self._permuted_elements)

