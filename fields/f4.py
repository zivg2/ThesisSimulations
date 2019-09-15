from itertools import product
from typing import Tuple, List

from . import FieldElement, Field
from .prime_field import PrimeField
from .f4_element import F4Element
from fields.field_with_product_table import FieldWithProductTable
from utilities.general_utilities import class_property_memorize, memorize


class F4(FieldWithProductTable):
    def __init__(self):
        self.base_field = PrimeField(2)
        self._product_table = {
            (ax, ay, bx, by):
                self.create_element((ax * bx + ay * by,
                                     ax * by + ay * bx + ay * by))
            for (ax, ay, bx, by) in product(self.base_field.get_all_elements(), repeat=4)
        }

    def create_element(self, element_pair: Tuple) -> F4Element:
        if isinstance(element_pair, F4Element) and element_pair.get_field() == self:
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
        return F4Element(x, y, self)

    def from_base_field_element(self, element: FieldElement) -> F4Element:
        return self.create_element((element, self.base_field.zero()))

    @class_property_memorize
    def zero(self) -> F4Element:
        return self.from_base_field_element(self.base_field.zero())

    @class_property_memorize
    def one(self) -> F4Element:
        return self.from_base_field_element(self.base_field.one())

    def extension_element(self) -> F4Element:
        return self.create_element((self.base_field.zero(), self.base_field.one()))

    def get_all_elements(self) -> List[FieldElement]:
        base_elements = self.base_field.get_all_elements()
        return [self.create_element(x) for x in product(base_elements, repeat=2)]

    def size(self) -> int:
        return self.base_field.size()**2

    def get_product(self, a, b) -> FieldElement:
        return self._product_table[(a.x, a.y, b.x, b.y)]

    def get_base_element(self, element: F4Element) -> FieldElement:
        return self.base_field.get_base_element(element.x)

    def trace(self, element: F4Element) -> FieldElement:
        return ((element ** self.base_field.size()) + element).x

    def norm(self, element: F4Element) -> FieldElement:
        return ((element ** self.base_field.size()) * element).x


