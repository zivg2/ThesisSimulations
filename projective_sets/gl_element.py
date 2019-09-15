from abc import ABC, abstractmethod

from fields import FieldElement
from utilities.general_utilities import class_property_memorize, memorize
from typing import Tuple


class GLElement(ABC):
    def __init__(self, coefficients: Tuple[Tuple[FieldElement, ...], ...], gl):
        self.gl = gl
        self.field = gl.get_field()
        self.coefficients = coefficients
        self.n = len(self.coefficients)

    @class_property_memorize
    def det(self) -> FieldElement:
        return GLElement.coefficients_det(self.coefficients)

    @staticmethod
    @memorize
    def coefficients_det(coefficients):
        if len(coefficients) == 1:
            return coefficients[0][0]
        factors = []
        for i in range(len(coefficients)):
            factors.append(coefficients[0][i]*GLElement.coefficients_det(tuple([x[:i] + x[i+1:] for x in coefficients[1:]])))
        s = 0
        for i in range(len(factors)):
            s += (-1) ** i * factors[i]
        return s

    @class_property_memorize
    def trace(self) -> FieldElement:
        return sum([self.coefficients[i][i] for i in range(self.n)])

    @class_property_memorize
    def inverse(self):
        self_det_inverse = self.det().inverse()
        coefficients = [[GLElement.coefficients_det([x[:j] + x[j+1:]
                                                     for x in self.coefficients[:i] + self.coefficients[i+1:]])
                         * self_det_inverse
                        for j in range(self.n)] for i in range(self.n)]
        return self.gl.create(coefficients)

    def __eq__(self, other):
        if not isinstance(other, GLElement):
            return False
        are_equal = True
        for i in range(self.n):
            for j in range(self.n):
                are_equal &= self.coefficients[i][j] == other.coefficients[i][j]
        return are_equal

    @class_property_memorize
    def __hash__(self):
        matrix = []
        for i in range(self.n):
            matrix += [self.coefficients[i][j] for j in range(self.n)]
        return tuple(matrix).__hash__()

    def matrix_str(self):
        return '(' + \
               ';'.join([','.join([str(x) for x in self.coefficients[i]])
                         for i in range(self.n)])\
               + ')'

    def __str__(self):
        return self.matrix_str()

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        coefficients = [[sum([self.coefficients[i][k] * other.coefficients[k][j]
                              for k in range(self.n)])
                         for j in range(other.n)]
                        for i in range(self.n)]
        return self.gl.create(coefficients)
