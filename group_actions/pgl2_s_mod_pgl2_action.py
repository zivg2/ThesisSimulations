from group_actions.finite_group_action import FiniteGroupAction
from utilities.general_utilities import measure
from elements_generator import ElementsGenerator, PermutationsElementsGenerator
from itertools import permutations
from math import factorial
from projective_sets.pgl2 import PGL2
from . import PGLGroupAction


class PGL2SModPGL2GroupAction(FiniteGroupAction):
    def __init__(self, q):
        self._q = q
        self._pgl2 = PGL2(q)
        self._pgl2_action = PGLGroupAction(self._pgl2)
        one = self._pgl2.get_field().one()
        self._fixed_values = [self._pgl2.get_pf().zero(),
                              self._pgl2.get_pf().create([one, one]),
                              self._pgl2.get_pf().infinity()]
        self._acted_upon_elements = list(permutations(range(2, self._q)))
        self._inverse_integral_value = {self._pgl2_action.get_integral_value(x): x
                                        for x in self._pgl2_action.get_acted_upon_elements()}

    def acted_upon_cardinality(self) -> int:
        return factorial(self._q-2)

    def get_acted_upon_elements(self):
        return list(permutations(range(2, self._q)))

    def get_acting_elements(self):
        return list(self._pgl2.get_all_elements())

    def get_elements_generator(self) -> ElementsGenerator:
        return self._pgl2

    @measure
    def apply(self, g, sigma):
        g_preimage_on_fixed_values = [self._pgl2_action.apply(g.inverse(), a) for a in self._fixed_values]
        values = [self.apply_permutation_inverse(sigma, a) for a in g_preimage_on_fixed_values]
        g2_inverse = self._pgl2.from_zero_one_infinity_values(values[0], values[1], values[2])
        result = [self._pgl2_action.apply(g2_inverse, self._inverse_integral_value[i]) for i in range(2, self._q)]
        result = [self.apply_permutation(sigma, x) for x in result]
        result = [self._pgl2_action.apply(g, x) for x in result]
        result = tuple([self._pgl2_action.get_integral_value(x) for x in result])
        return result

    def apply_permutation(self, permutation, x):
        if x in self._fixed_values:
            return x
        i = self._pgl2_action.get_integral_value(x)
        j = permutation[i-2]
        return self._inverse_integral_value[j]

    def apply_permutation_inverse(self, permutation, x):
        if x in self._fixed_values:
            return x
        i = self._pgl2_action.get_integral_value(x)
        j = permutation.index(i)
        return self._inverse_integral_value[j+2]

    @measure
    def get_integral_value(self, x):
        return self._acted_upon_elements.index(x)
