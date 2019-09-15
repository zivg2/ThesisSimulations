from elements_generator import ElementsGenerator
from fields import FieldFromInteger, FieldElement, Field
from projective_sets.pf_element import PFElement
from typing import List
from itertools import product


class PF(ElementsGenerator[PFElement]):
    def __init__(self, n, q):
        self._field = FieldFromInteger.from_q(q)
        self.n = n

    def create(self, x: List[FieldElement]):
        return PFElement(x, self._field)

    def get_all_elements(self) -> List[PFElement]:
        elements = []
        for i in range(self.n):
            remainder = product(self._field.get_all_elements(), repeat=self.n-i-1)
            for x in remainder:
                elements.append(list(x) + [self._field.one()] + [self._field.zero()] * i)
        elements = [self.create(x) for x in elements]
        return elements

    def get_field(self) -> Field:
        return self._field

    def zero(self):
        return self.create([self._field.zero()] * (self.n-1) + [self._field.one()])

    def infinity(self):
        return self.create([self._field.one()] + [self._field.zero()] * (self.n-1))

    def __str__(self):
        return "P%d(%s)" % (self.n, str(self._field))
