from abc import ABC, abstractmethod

from fields import FieldElement
from utilities.general_utilities import class_property_memorize, memorize
from typing import Tuple


class PGLElement(ABC):
    def __init__(self, coefficients: Tuple[Tuple[FieldElement, ...], ...], pgl):
        self.pgl = pgl
        self.field = pgl.get_field()
        self.coefficients = coefficients
        self.n = len(self.coefficients)

    @class_property_memorize
    def det(self) -> FieldElement:
        return PGLElement.coefficients_det(self.coefficients)

    @staticmethod
    @memorize
    def coefficients_det(coefficients):
        if len(coefficients) == 1:
            return coefficients[0][0]
        factors = []
        for i in range(len(coefficients)):
            factors.append(coefficients[0][i]*PGLElement.coefficients_det(tuple([x[:i] + x[i+1:] for x in coefficients[1:]])))
        s = 0
        for i in range(len(factors)):
            s += (-1) ** i * factors[i]
        return s

    @class_property_memorize
    def trace(self) -> FieldElement:
        return sum([self.coefficients[i][i] for i in range(self.n)])

    @class_property_memorize
    def inverse(self):
        coefficients = [[PGLElement.coefficients_det([x[:j] + x[j+1:]
                                                      for x in self.coefficients[:i] + self.coefficients[i+1:]])
                        for j in range(self.n)] for i in range(self.n)]
        return self.pgl.create(coefficients)

    def __eq__(self, other):
        if not isinstance(other, PGLElement):
            return False
        for k in range(self.n-1, -1, -1):
            if self.coefficients[self.n-1][k] != self.field.zero():
                if other.coefficients[self.n-1][k] == self.field.zero():
                    return False
                x1 = self.coefficients[self.n-1][k]
                x2 = other.coefficients[self.n-1][k]
                are_equal = True
                for i in range(self.n):
                    for j in range(self.n):
                        are_equal &= x2*self.coefficients[i][j] == x1*other.coefficients[i][j]
                return are_equal
        return False

    @class_property_memorize
    def __hash__(self):
        for k in range(self.n-1, -1, -1):
            if self.coefficients[self.n-1][k] != self.field.zero():
                divisor = self.coefficients[self.n-1][k].inverse()
                matrix = []
                for i in range(self.n):
                    matrix += [self.coefficients[i][j]*divisor for j in range(self.n)]
                return tuple(matrix).__hash__()
        return 0

    def matrix_str(self):
        return '[' + \
               ';'.join([','.join([str(x) for x in self.coefficients[i]])
                         for i in range(self.n)])\
               + ']'

    def __str__(self):
        return self.matrix_str()

    def __repr__(self):
        return str(self)

    def __mul__(self, other):
        coefficients = [[sum([self.coefficients[i][k] * other.coefficients[k][j]
                              for k in range(self.n)], self.field.zero())
                         for j in range(other.n)]
                        for i in range(self.n)]
        return self.pgl.create(coefficients)
