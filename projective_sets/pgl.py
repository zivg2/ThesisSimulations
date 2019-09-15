from abc import abstractmethod
from typing import List
from itertools import product

from elements_generator import ElementsGenerator
from fields import FieldElement, Field
from projective_sets.pf import PF
from projective_sets.pgl_element import PGLElement
from projective_sets.pgl2_element import PGL2Element
from utilities.general_utilities import class_property_memorize, measure


class PGL(ElementsGenerator[PGLElement]):
    def __init__(self, n, q):
        self._q = q
        self._n = n
        self._pf = PF(n, q)
        self._field = self._pf.get_field()

    def create(self, coefficients: List[List[FieldElement]]) -> PGLElement:
        if self._n == 2:
            return PGL2Element(coefficients[0][0], coefficients[0][1], coefficients[1][0], coefficients[1][1],
                               self)
        else:
            coefficients_tuple = tuple([tuple(x) for x in coefficients])
            return PGLElement(coefficients_tuple, self)

    @class_property_memorize
    def identity(self):
        field = self._field
        coefficients = [[field.one() if i == j else field.zero() for j in range(self._n)] for i in range(self._n)]
        return self.create(coefficients)

    def get_all_elements(self) -> List[PGLElement]:
        elements = []
        for i in range(1, self._n + 1):
            for x in product(self._field.get_all_elements(), repeat=self._n - i):
                first_row = [self._field.zero()] * (i-1) + [self._field.one()] + list(x)
                for rows_tuples in product(product(self._field.get_all_elements(), repeat=self._n), repeat=self._n - 1):
                    rows = [list(reversed(row)) for row in rows_tuples]
                    matrix = self.create([first_row] + rows)
                    if matrix.det() != self._field.zero():
                        elements.append(matrix)
        return elements

    def random_element(self) -> PGLElement:
        finished = False
        while not finished:
            coefficients = [[self._field.random_element() for _ in range(self._n)] for _ in range(self._n)]
            matrix = self.create(coefficients)
            finished = matrix.det() != self._field.zero()
        return matrix

    def q(self) -> int:
        return self._q

    def get_pf(self) -> PF:
        return self._pf

    def get_field(self) -> Field:
        return self._field

    def __str__(self):
        return "PGL%d(%d)" % (self._n, self._q)
