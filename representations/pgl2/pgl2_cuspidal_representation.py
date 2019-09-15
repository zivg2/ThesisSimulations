import numpy as np
from representations import Representation
from utilities.general_utilities import *
from representations.characters import Character
from representations.characters.representation_character import RepresentationCharacter
from fields.square_extension_field import SquareExtensionField
from fields.field_multiplicative_group import FieldMultiplicativeGroup
from projective_sets.pgl2 import PGL2, PGL2Element
from representations.characters.field_character import FieldCharacter, Field, FieldElement
from representations.characters.pgl2.pgl2_cuspidal_character import PGL2CuspidalCharacter


class PGL2CuspidalRepresentation(Representation):
    def __init__(self, pgl2: PGL2, k):
        self._pgl2 = pgl2
        self._base_field = pgl2.get_field()
        self._q = self._base_field.size()
        assert(0 < k < self._q / 2)
        self.square_field = SquareExtensionField.from_base_field(self._base_field)
        self.square_field_character = FieldCharacter(self.square_field, k, self._q + 1)
        self.multiplicative_group = FieldMultiplicativeGroup.from_field(self.square_field)
        self.representatives_by_index = [self.multiplicative_group.get_element(i) for i in range(self._q - 1)]
        self.representative_index_by_field_element = {}
        for i in range(self._q-1):
            self.representative_index_by_field_element[self.square_field.norm(self.representatives_by_index[i])] = i
        self.norm_one_elements = [self.multiplicative_group.get_element(i) for i in range(0, self._q**2-1, self._q-1)]

    def _apply_additive_character(self, x: FieldElement):
        element = self._base_field.get_base_element(x)
        return FieldCharacter.get_nth_unity_root(element.n, element.get_field().size())

    @measure
    @memorize
    def apply(self, g: PGL2Element):
        if g.c == 0:
            return self.apply_on_upper(g)
        else:
            return self.apply_on_non_upper(g)

    def apply_on_upper(self, g: PGL2Element):
        result = np.zeros((self.dim(), self.dim()), dtype=complex)
        for j in range(self.dim()):
            t = self.square_field.norm(self.representatives_by_index[j])
            i = self.representative_index_by_field_element[g.a/g.d*t]
            d_in_square = self.square_field.from_base_field_element(g.d)
            value = self._apply_additive_character(g.b/g.d*t)
            value *= self.square_field_character.apply(d_in_square.inverse() *
                                                       self.representatives_by_index[j] /
                                                       self.representatives_by_index[i])
            result[j, i] = value
        return result

    def apply_on_non_upper(self, g: PGL2Element):
        result = np.zeros((self.dim(), self.dim()), dtype=complex)
        for j in range(self.dim()):
            for i in range(self.dim()):
                t = self.square_field.norm(self.representatives_by_index[i])
                s = self.square_field.norm(self.representatives_by_index[j])
                delta_index = self.representative_index_by_field_element[g.det()]
                trace_coefficient = (self.representatives_by_index[i]) ** self._q
                trace_coefficient *= self.representatives_by_index[j]
                trace_coefficient *= self.representatives_by_index[delta_index]
                value = sum([(self.square_field_character.apply(y)) *
                             self._apply_additive_character(-self.square_field.trace(trace_coefficient * y)/g.c)
                             for y in self.norm_one_elements])
                value *= self._apply_additive_character((g.a*t + g.d*s)/g.c)
                value /= -self._q
                value *= self.square_field_character.apply(self.representatives_by_index[delta_index])
                result[i, j] = value
        return result

    def get_character(self) -> Character:
        return PGL2CuspidalCharacter(self._base_field.size(), self.square_field_character)

    def dim(self):
        return self._q-1

    def __str__(self):
        return 'cusp(%s)' % self.square_field_character
