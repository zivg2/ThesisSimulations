from itertools import product

from projective_sets.pgl import PGL
from typing import List

from .pf import PF
from .pgl2_element import PGL2Element
from .pf2_element import PF2Element
from fields import SquareExtensionField, FieldElement
from utilities.general_utilities import class_property_memorize, memorize, measure
from elements_generator import ElementsGenerator, IterableElementsGenerator

from typing import Dict


class PGL2(PGL, ElementsGenerator[PGL2Element]):
    def __init__(self, q):
        super().__init__(2, q)
        self._square_extension = SquareExtensionField.from_base_field(self._field)
        self._ratios = []
        self._square_diagonalizable_ys = []

    @measure
    @class_property_memorize
    def get_all_elements(self) -> List[PGL2Element]:
        elements = [self.create2(self._field.one(), a, b, c) for
                    (a, b, c) in product(self._field.get_all_elements(), repeat=3) if c != a * b]
        elements.extend([self.create2(self._field.zero(), self._field.one(), a, b) for
                         (a, b) in product(self._field.get_all_elements(), repeat=2) if a != self._field.zero()])
        return elements

    @measure
    def create2(self, a: FieldElement, b: FieldElement, c: FieldElement, d: FieldElement) -> PGL2Element:
        return PGL2Element(a, b, c, d, self)

    def smaller_pgl2(self, q2) -> ElementsGenerator[PGL2Element]:
        smaller_pf2 = PF(2, q2)
        smaller_field = smaller_pf2.get_field()
        elements_tuples = [(smaller_field.one(), a, b, c) for
                           (a, b, c) in product(smaller_field.get_all_elements(), repeat=3) if c != a * b]
        elements_tuples.extend([(smaller_field.zero(), smaller_field.one(), a, b) for
                                (a, b) in product(smaller_field.get_all_elements(), repeat=2) if a != self._field.zero()])
        elements_tuples = [(self._field.from_base_field_element(a), self._field.from_base_field_element(b),
                           self._field.from_base_field_element(c), self._field.from_base_field_element(d))
                           for a, b, c, d in elements_tuples]
        elements = [self.create2(a, b, c, d) for a, b, c, d in elements_tuples]
        return IterableElementsGenerator(elements, "PGL2(%d)" % q2)

    def from_zero_one_infinity_values(self, x: PF2Element, y: PF2Element, z: PF2Element) -> PGL2Element:
        zero_coefficient = PF2Element.det(y, z)
        infinity_coefficient = PF2Element.det(x, y)
        return self.create2(infinity_coefficient * z[0], zero_coefficient * x[0],
                            infinity_coefficient * z[1], zero_coefficient * x[1])

    @class_property_memorize
    def unipotent(self):
        field = self._field
        return self.create2(field.one(), field.one(), field.zero(), field.one())

    def diagonalizable(self, ratio):
        if ratio in self._ratios:
            field = self._field
            return self.create2(ratio, field.zero(), field.zero(), field.one())
        elif ratio.inverse() in self._ratios:
            field = self._field
            return self.create2(ratio.inverse(), field.zero(), field.zero(), field.one())
        else:
            self._ratios.append(ratio)
            field = self._field
            return self.create2(ratio, field.zero(), field.zero(), field.one())

    def square_diagonalizable(self, x, y):
        if y in self._square_diagonalizable_ys or x == self._field.zero():
            delta = SquareExtensionField.get_non_square_element(self._field)
            return self.create2(x, delta * y, y, x)
        elif -y in self._square_diagonalizable_ys:
            delta = SquareExtensionField.get_non_square_element(self._field)
            return self.create2(x, -delta * y, -y, x)
        else:
            self._square_diagonalizable_ys.append(y)
            delta = SquareExtensionField.get_non_square_element(self._field)
            return self.create2(x, delta * y, y, x)

    def get_conjugation_classes(self) -> Dict[PGL2Element, int]:
        classes = dict()
        zero = self._field.zero()
        one = self._field.one()
        classes[self.identity()] = 1
        classes[self.unipotent()] = self._q * self._q - 1

        used_x = [one, zero, -one]
        for x in self._field.get_all_elements():
            if x in used_x or x.inverse() in used_x:
                continue
            classes[self.diagonalizable(x)] = self._q * (self._q + 1)
            used_x.append(x)

        classes[self.diagonalizable(-one)] = (self._q * (self._q + 1)) // 2
        used_y = [zero]
        for y in self._field.get_all_elements():
            if y in used_y or -y in used_y:
                continue
            classes[self.square_diagonalizable(one, y)] = (self._q * (self._q - 1))
            used_y.append(y)

        classes[self.square_diagonalizable(zero, one)] = (self._q * (self._q - 1)) // 2
        return classes

    @memorize
    def get_conjugation_class(self, x: PGL2Element):
        discriminant = x.trace() * x.trace() - 4 * x.det()
        is_square = discriminant.legendre()
        if is_square == 0:
            if x.b == self._field.zero() and x.c == self._field.zero():
                return self.identity()
            else:
                return self.unipotent()
        elif is_square == 1:
            discriminant_sqrt = discriminant.sqrt()
            ratio = (x.trace() + discriminant_sqrt) / (x.trace() - discriminant_sqrt)
            return self.diagonalizable(ratio)
        else:
            discriminant_sqrt = self._square_extension.from_base_field_element(discriminant).sqrt()
            z_base = self._square_extension.from_base_field_element(x.trace())
            field_two = self._square_extension.one() + self._square_extension.one()
            z = (z_base + discriminant_sqrt) / field_two
            if z.x != self._field.zero():
                return self.square_diagonalizable(self._field.one(), z.y/z.x)
            else:
                return self.square_diagonalizable(self._field.zero(), self._field.one())

