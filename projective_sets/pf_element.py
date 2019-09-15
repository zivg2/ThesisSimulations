from fields import FieldElement, Field
from utilities.general_utilities import measure
from typing import List
from utilities.general_utilities import class_property_memorize


class PFElement:
    def __init__(self, x: List[FieldElement], field: Field):
        self._x = x
        self._n = len(x)
        self._field = field

    @class_property_memorize
    def last_nonzero_index(self):
        for k in range(self._n-1, -1, -1):
            if self._x[k] != self._field.zero():
                return k
        return -1

    @measure
    def __eq__(self, other):
        if not isinstance(other, PFElement):
            return False
        for k in range(self._n-1, -1, -1):
            if self._x[k] != self._field.zero():
                if other._x[k] == self._field.zero():
                    return False
                x1 = self._x[k]
                x2 = other._x[k]
                are_equal = True
                for i in range(self._n):
                    are_equal &= x2*self._x[i] == x1*other._x[i]
                return are_equal
        return False

    def __hash__(self):
        for k in range(self._n-1, -1, -1):
            if self._x[k] != self._field.zero():
                divisor = self._x[k].inverse()
                vector = tuple([self._x[i]*divisor for i in range(self._n)])
                return vector.__hash__()
        return 0

    def __str__(self):
        k = self.last_nonzero_index()
        divisor = self._x[k].inverse()
        vector = tuple([self._x[i]*divisor for i in range(self._n)])
        return str(vector)

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self._x[key]
