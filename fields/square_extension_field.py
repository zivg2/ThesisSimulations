from typing import Tuple, List

from . import FieldElement, Field
from .square_extension_field_element import SquareExtensionFieldElement
from fields.field_with_product_table import FieldWithProductTable
from utilities.general_utilities import class_property_memorize, memorize
from itertools import product


class SquareExtensionField(FieldWithProductTable):
    def __init__(self, base_field: Field, non_square_element: FieldElement):
        self.base_field = base_field
        self.non_square_element = non_square_element
        self._product_table = {
            (ax, ay, bx, by):
                self.create_element((ax * bx + self.non_square_element * ay * by,
                                     ax * by + ay * bx))
            for (ax, ay, bx, by) in product(self.base_field.get_all_elements(), repeat=4)
        }

    @classmethod
    @memorize
    def from_base_field(cls, base_field: Field):
        non_square_element = SquareExtensionField.get_non_square_element(base_field)
        return cls(base_field, non_square_element)

    @staticmethod
    @memorize
    def get_non_square_element(base_field):
        if base_field.size() % 4 == 3:
            return -base_field.one()
        non_square_element = next(x for x in base_field.get_all_elements() if x.legendre() == -1)
        return non_square_element

    def create_element(self, element_pair: Tuple) -> SquareExtensionFieldElement:
        if isinstance(element_pair, SquareExtensionFieldElement) and element_pair.get_field() == self:
            return element_pair

        if isinstance(element_pair, int):
            x = self.base_field.create_element(element_pair)
            y = self.base_field.zero()
        elif isinstance(element_pair, FieldElement):
            x = element_pair
            y = self.base_field.zero()
        elif isinstance(element_pair[0], FieldElement):
            x = element_pair[0]
            y = element_pair[1]
        else:
            x = self.base_field.create_element(element_pair[0])
            y = self.base_field.create_element(element_pair[1])
        return SquareExtensionFieldElement(x, y, self)

    def from_base_field_element(self, element: FieldElement) -> SquareExtensionFieldElement:
        return self.create_element((element, self.base_field.zero()))

    @class_property_memorize
    def zero(self):
        return self.from_base_field_element(self.base_field.zero())

    @class_property_memorize
    def one(self):
        return self.from_base_field_element(self.base_field.one())

    def extension_element(self):
        return self.create_element((self.base_field.zero(), self.base_field.one()))

    def get_all_elements(self) -> List[FieldElement]:
        base_elements = self.base_field.get_all_elements()
        return [self.create_element(x) for x in product(base_elements, repeat=2)]

    def size(self) -> int:
        return self.base_field.size()**2

    def get_product(self, a, b) -> FieldElement:
        return self._product_table[(a.x, a.y, b.x, b.y)]

    def get_base_element(self, element: SquareExtensionFieldElement) -> FieldElement:
        return self.base_field.get_base_element(element.x)

    def trace(self, element: SquareExtensionFieldElement) -> FieldElement:
        return ((element ** self.base_field.size()) + element).x

    def norm(self, element: SquareExtensionFieldElement) -> FieldElement:
        return ((element ** self.base_field.size()) * element).x


