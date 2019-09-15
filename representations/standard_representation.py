import numpy as np
from . import Representation
from utilities.general_utilities import *
from group_actions.finite_group_action import FiniteGroupAction
from .characters import Character
from .characters.representation_character import RepresentationCharacter


class StandardRepresentation(Representation):
    def __init__(self, action: FiniteGroupAction, special_value):
        self._action = action
        self._dim = self._action.acted_upon_cardinality() - 1
        self._special_value = special_value
        self._MINUS_ONES = -np.ones(self._dim).transpose()

    @measure
    @memorize
    def apply(self, g):
        result = self._apply_normal_values(g)

        special_value_action_result = self._action.apply(g, self._special_value)
        if special_value_action_result != self._special_value:
            i = self._action.get_integral_value(special_value_action_result)
            result[i, :] = self._MINUS_ONES

        return result

    @measure
    def _apply_normal_values(self, g):
        result = np.zeros((self._dim, self._dim))
        for value in self._action.get_acted_upon_elements():
            if value == self._special_value:
                continue

            action_result = self._action.apply(g, value)

            if action_result != self._special_value:
                i = self._action.get_integral_value(action_result)
                j = self._action.get_integral_value(value)
                result[i, j] = 1

        return result

    def get_character(self) -> Character:
        return RepresentationCharacter(self)

    def dim(self):
        return self._dim

    def __str__(self):
        return 'std'
