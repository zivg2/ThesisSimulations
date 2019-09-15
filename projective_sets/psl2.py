from itertools import product

from .pgl2_element import PGL2Element
from .pgl2 import PGL2
from fields import SquareExtensionField, FieldElement
from utilities.general_utilities import measure, class_property_memorize
import random

from typing import List, Dict


class PSL2(PGL2):
    def __init__(self, q):
        super().__init__(q)

    @staticmethod
    def is_determinant_square(x: PGL2Element):
        return x.det().legendre() == 1

    @measure
    @class_property_memorize
    def get_all_elements(self) -> List[PGL2Element]:
        elements = [self.create2(self._field.one(), a, b, c) for
                    (a, b, c) in product(self._field.get_all_elements(), repeat=3) if c != a * b]
        elements.extend([self.create2(self._field.zero(), self._field.one(), a, b) for
                         (a, b) in product(self._field.get_all_elements(), repeat=2) if a != self._field.zero()])
        elements = [x for x in elements if self.is_determinant_square(x)]
        return elements

    def random_element(self) -> PGL2Element:
        field_elements = self._field.get_all_elements()
        finished = False
        while not finished:
            a, b, c, d = (random.choice(field_elements) for _ in range(4))
            finished = (a*d - b*c).legendre() == 1
        return self.create2(a, b, c, d)

    def get_conjugation_classes(self) -> Dict[PGL2Element, int]:
        classes = dict()
        zero = self._field.zero()
        one = self._field.one()
        delta = SquareExtensionField.get_non_square_element(self._field)

        classes[self.create2(one, zero, zero, one)] = 1
        classes[self.create2(one, one, zero, one)] = (self._q * self._q - 1) // 2
        classes[self.create2(one, delta, zero, one)] = (self._q * self._q - 1) // 2

        used_x = [one, zero, -one]
        for x in self._field.get_all_elements():
            if x in used_x or x.inverse() in used_x or -x in used_x or -x.inverse() in used_x:
                continue
            if x.inverse() != -x:
                classes[self.create2(x, zero, zero, x.inverse())] = self._q * (self._q + 1)
            else:
                classes[self.create2(x, zero, zero, x.inverse())] = self._q * (self._q + 1) // 2
            used_x.append(x)

        used_y = [zero]
        for y in self._field.get_all_elements():
            if y in used_y or -y in used_y:
                continue
            x_square = delta * y * y + one
            if x_square.legendre() != 1:
                continue
            x = x_square.sqrt()
            classes[self.create2(x, delta * y, y, x)] = (self._q * (self._q - 1))
            used_y.append(y)

        if self._q % 4 == 3:
            classes[self.create2(zero, delta, one, zero)] = (self._q * (self._q - 1)) // 2

        return classes

    def __str__(self):
        return "PSL2(%d)" % self._q

