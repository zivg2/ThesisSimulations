from group_actions.finite_group_action import FiniteGroupAction
from projective_sets.pf_element import PFElement
from projective_sets.pgl import PGL
from projective_sets.pgl_element import PGLElement
from utilities.general_utilities import measure


class PGLGroupAction(FiniteGroupAction):
    def __init__(self, pgl: PGL):
        self._pgl = pgl
        self._pf = pgl.get_pf()

    def acted_upon_cardinality(self) -> int:
        q = self._pgl.q()
        return sum([q**i for i in range(self._pf.n)])

    def get_acted_upon_elements(self):
        return self._pf.get_all_elements()

    def get_acting_elements(self):
        return self._pgl.get_all_elements()

    @measure
    def apply(self, g: PGLElement, x: PFElement):
        result = [sum([g.coefficients[i][k] * x[k] for k in range(self._pf.n)]) for i in range(self._pf.n)]
        return self._pf.create(result)

    @measure
    def get_integral_value(self, x: PFElement) -> int:
        if x == self._pf.infinity():
            return self.acted_upon_cardinality()-1
        i = x.last_nonzero_index()
        c = x[i].inverse()
        return sum([int(c*x[j]) * (self._pgl.q() ** j) for j in range(i)])

