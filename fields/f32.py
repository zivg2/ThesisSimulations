from itertools import product
from typing import Tuple, List

from . import FieldElement
from .prime_field import PrimeField
from .f32_element import F32Element
from fields.field_with_product_table import FieldWithProductTable
from utilities.general_utilities import class_property_memorize


class F32(FieldWithProductTable):
    COEFFICIENTS_LENGTH = 5

    def __init__(self):
        self.base_field = PrimeField(2)
        self._product_table = {
            ((a0, a1, a2, a3, a4),
             (b0, b1, b2, b3, b4)):
                 self.create_element((
                     self.multiply((a0, a1, a2, a3, a4), (b0, b1, b2, b3, b4))
                 ))
            for (a0, a1, a2, a3, a4,
                 b0, b1, b2, b3, b4) in product(self.base_field.get_all_elements(), repeat=10)
        }

    def multiply(self, a, b):
        coefficients = [sum(
                            [a[j]*b[i-j] for j in range(max(0, i + 1 - len(b)), min(i+1, len(a)))],
                            self.base_field.zero())
                        for i in range(0, len(a) + len(b))
        ]

        while len(coefficients) > F32.COEFFICIENTS_LENGTH:
            extra_coefficients = coefficients[F32.COEFFICIENTS_LENGTH:]
            coefficients = coefficients[:F32.COEFFICIENTS_LENGTH]
            while len(coefficients) < len(extra_coefficients) + 2:
                coefficients.append(self.base_field.zero())
            while len(extra_coefficients) < len(coefficients):
                extra_coefficients.append(self.base_field.zero())
            for i in range(len(coefficients)):
                coefficients[i] += extra_coefficients[i]
                if i >= 2:
                    coefficients[i] += extra_coefficients[i-2]
            while len(coefficients) > F32.COEFFICIENTS_LENGTH and coefficients[-1] == self.base_field.zero():
                coefficients.pop(-1)

        return tuple(coefficients)

    def create_element(self, element_tuple: Tuple) -> F32Element:
        if isinstance(element_tuple, F32Element) and element_tuple.get_field() == self:
            return element_tuple

        if isinstance(element_tuple, int):
            x = [self.base_field.create_element(element_tuple)] + \
                [self.base_field.zero()] * (F32.COEFFICIENTS_LENGTH - 1)
        elif isinstance(element_tuple, FieldElement):
            x = [element_tuple] + [self.base_field.zero()] * (F32.COEFFICIENTS_LENGTH - 1)
        elif isinstance(element_tuple[0], FieldElement):
            x = element_tuple
        else:
            x = [self.base_field.create_element(element_tuple[i]) for i in range(len(element_tuple))]
        return F32Element(tuple(x), self)

    def from_base_field_element(self, element: FieldElement) -> F32Element:
        element_tuple = [element] + [self.base_field.zero()] * (F32.COEFFICIENTS_LENGTH - 1)
        return self.create_element(tuple(element_tuple))

    @class_property_memorize
    def zero(self):
        return self.from_base_field_element(self.base_field.zero())

    @class_property_memorize
    def one(self):
        return self.from_base_field_element(self.base_field.one())

    def get_all_elements(self) -> List[FieldElement]:
        base_elements = self.base_field.get_all_elements()
        return [self.create_element(x) for x in product(base_elements, repeat=5)]

    def size(self) -> int:
        return self.base_field.size()**F32.COEFFICIENTS_LENGTH

    def get_product(self, a, b) -> FieldElement:
        return self._product_table[(a.coefficients, b.coefficients)]

    def get_base_element(self, element: F32Element) -> FieldElement:
        return self.base_field.get_base_element(element.coefficients[0])

    def trace(self, element: F32Element) -> FieldElement:
        trace1 = sum([element ** (2 ** i) for i in range(0, F32.COEFFICIENTS_LENGTH)])
        return trace1.coefficients[0]

    def norm(self, element: F32Element) -> FieldElement:
        norm1 = element ** 31
        return norm1.coefficients[0]


