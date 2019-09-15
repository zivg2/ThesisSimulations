import numpy as np
from utilities.general_utilities import memorize, measure
from . import StandardRepresentation, UnitaryRepresentation
from group_actions.pgl2_group_action import PGLGroupAction, FiniteGroupAction


def get_pgl2_unitary_standard_representation(pgl2):
    return TransitiveActionUnitaryStandardRepresentation(PGLGroupAction(pgl2), pgl2.get_pf().infinity())


class TransitiveActionUnitaryStandardRepresentation(UnitaryRepresentation):
    def __init__(self, action: FiniteGroupAction, special_value):
        self._action = action
        self._special_value = special_value
        super().__init__(StandardRepresentation(action, special_value))

    def _calculate_conjugation_constants(self):
        d = self.dim()
        i_matrix = np.eye(d)
        j_matrix = np.ones(d)
        conjugation_constant = i_matrix + (np.sqrt(d + 1) - 1) / d * j_matrix
        conjugation_inverse = i_matrix + (1 / np.sqrt(d + 1) - 1) / d * j_matrix
        conjugation_constant *= (np.sqrt(d / (d + 1)))
        conjugation_inverse *= (np.sqrt((d + 1) / d))
        return conjugation_constant, conjugation_inverse

    @memorize
    def apply(self, g):
        non_conjugated_value = self._representation.apply(g)
        if self._action.apply(g, self._special_value) == self._special_value:
            return non_conjugated_value

        return super().apply(g)

    @measure
    def apply_obsolete(self, g) -> np.ndarray:
        non_conjugated_value = self._representation.apply(g)
        if self._action.apply(g, self._special_value) == self._special_value:
            return non_conjugated_value

        d = self.dim()
        t = (np.sqrt(d+1)-1)/d

        ones = np.ones(non_conjugated_value.shape)
        result = non_conjugated_value - t*t*ones

        i = self._action.get_integral_value(self._action.apply(g, self._special_value))
        result[i, :] += (1-t)*ones[i, :]

        j = self._action.get_integral_value(self._inverse_special_value(g))
        result[:, j] -= t*ones[:, j]

        return result

    @memorize
    def _inverse_special_value(self, g):
        for x in self._action.get_acted_upon_elements():
            if self._action.apply(g, x) == self._special_value:
                return x
        raise AssertionError()
