from abc import abstractmethod
from typing import List
from itertools import product

from elements_generator import ElementsGenerator
from fields import FieldElement, Field, FieldFromInteger
from projective_sets.gl_element import GLElement
from utilities.general_utilities import class_property_memorize, measure


class GL(ElementsGenerator[GLElement]):
    def __init__(self, n, q):
        self._q = q
        self._n = n
        self._field = FieldFromInteger.from_q(q)

    def create(self, coefficients: List[List[FieldElement]]) -> GLElement:
        coefficients_tuple = tuple([tuple(x) for x in coefficients])
        return GLElement(coefficients_tuple, self)

    @class_property_memorize
    def identity(self):
        field = self._field
        coefficients = [[field.one() if i == j else field.zero() for j in range(self._n)] for i in range(self._n)]
        return self.create(coefficients)

    def get_all_elements(self) -> List[GLElement]:
        elements = []
        for rows_tuples in product(product(self._field.get_all_elements(), repeat=self._n), repeat=self._n):
            rows = [list(reversed(row)) for row in rows_tuples]
            matrix = self.create(rows)
            if matrix.det() != self._field.zero():
                elements.append(matrix)
        return elements

    def random_element(self) -> GLElement:
        finished = False
        while not finished:
            coefficients = [[self._field.random_element() for _ in range(self._n)] for _ in range(self._n)]
            matrix = self.create(coefficients)
            finished = matrix.det() != self._field.zero()
        return matrix

    def q(self) -> int:
        return self._q

    def get_field(self) -> Field:
        return self._field

    def __str__(self):
        return "GL%d(%d)" % (self._n, self._q)
