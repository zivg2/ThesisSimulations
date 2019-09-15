from itertools import product
from group_actions.finite_group_action import FiniteGroupAction
from utilities.general_utilities import measure
from itertools import permutations


class D2NGroupAction(FiniteGroupAction):
    def __init__(self, n):
        self._n = n

    def acted_upon_cardinality(self) -> int:
        return self._n

    def get_acted_upon_elements(self):
        return list(range(self._n))

    def get_acting_elements(self):
        return list(product(range(self._n), range(2)))

    @measure
    def apply(self, g, x):
        i = g[0]
        j = 1 if g[1] == 0 else -1
        return (j * (i + x)) % self._n

    @measure
    def get_integral_value(self, x):
        return x
