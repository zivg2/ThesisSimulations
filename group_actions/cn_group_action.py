from group_actions.finite_group_action import FiniteGroupAction
from utilities.general_utilities import measure
from itertools import permutations


class CNGroupAction(FiniteGroupAction):
    def __init__(self, n):
        self._n = n

    def acted_upon_cardinality(self) -> int:
        return self._n

    def get_acted_upon_elements(self):
        return list(range(self._n))

    def get_acting_elements(self):
        return list(range(self._n))

    @measure
    def apply(self, g, x):
        return (g + x) % self._n

    @measure
    def get_integral_value(self, x):
        return x
