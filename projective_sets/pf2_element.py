from projective_sets.pf_element import PFElement
from utilities.general_utilities import measure
from fields import FieldElement, Field


class PF2Element(PFElement):
    def __init__(self, x0: FieldElement, x1: FieldElement, field: Field):
        super().__init__([x0, x1], field)

    @measure
    def __eq__(self, other):
        return isinstance(other, PF2Element) and PF2Element.det(self, other) == self._field.zero()

    @staticmethod
    @measure
    def det(element1, element2):
        return element1[0] * element2[1] - element1[1] * element2[0]

    @measure
    def to_field_element(self):
        return self._x[1] / self._x[0]

    def __str__(self):
        if self._x[0] != self._field.zero():
            return str(self._x[1] / self._x[0])
        else:
            return 'inf'

