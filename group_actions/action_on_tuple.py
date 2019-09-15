from group_actions.finite_group_action import FiniteGroupAction
from utilities.general_utilities import measure
from scipy.misc import comb, factorial
from itertools import permutations


class ActionOnTuple(FiniteGroupAction):
    def __init__(self, base_action: FiniteGroupAction, k):
        self._k = k
        self._base_action = base_action
        self._acted_upon_elements = list(permutations(self._base_action.get_acted_upon_elements(), r=self._k))

    def acted_upon_cardinality(self) -> int:
        n = self._base_action.acted_upon_cardinality()
        return int(comb(n, self._k) * factorial(self._k))

    def get_acted_upon_elements(self):
        base_acted_upon_elements = self._base_action.get_acted_upon_elements()
        return list(permutations(base_acted_upon_elements, r=self._k))

    def get_acting_elements(self):
        return self._base_action.get_acting_elements()

    @measure
    def apply(self, g, x):
        return tuple([self._base_action.apply(g, a) for a in x])

    @measure
    def get_integral_value(self, x):
        return self._acted_upon_elements.index(x)
