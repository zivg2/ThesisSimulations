from group_actions.finite_group_action import FiniteGroupAction
from utilities.general_utilities import measure
from elements_generator import ElementsGenerator, PermutationsElementsGenerator
from itertools import permutations


class SNGroupAction(FiniteGroupAction):
    def __init__(self, n):
        self._n = n

    def acted_upon_cardinality(self) -> int:
        return self._n

    def get_acted_upon_elements(self):
        return list(range(self._n))

    def get_acting_elements(self):
        return list(permutations(self.get_acted_upon_elements()))

    def get_elements_generator(self) -> ElementsGenerator:
        return PermutationsElementsGenerator(self.get_acted_upon_elements())

    @measure
    def apply(self, g, x):
        return g[x]

    @measure
    def get_integral_value(self, x):
        return x
