import numpy as np
from . import Representation
from utilities.general_utilities import *
from group_actions.finite_group_action import FiniteGroupAction
from .characters import Character
from .characters.representation_character import RepresentationCharacter


class PermutationRepresentation(Representation):
    def __init__(self, action: FiniteGroupAction):
        self._action = action
        self._dim = self._action.acted_upon_cardinality()

    @measure
    @memorize
    def apply(self, g):
        result = np.zeros((self._dim, self._dim))
        for value in self._action.get_acted_upon_elements():
            action_result = self._action.apply(g, value)
            i = self._action.get_integral_value(action_result)
            j = self._action.get_integral_value(value)
            result[i, j] = 1

        return result

    def get_character(self) -> Character:
        return RepresentationCharacter(self)

    def dim(self):
        return self._dim

    def __str__(self):
        return 'perm'
