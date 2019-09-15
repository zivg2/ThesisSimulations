from . import FieldElement
from utilities.general_utilities import class_property_memorize, measure, memorize
from typing import Tuple, Iterable


class F32Element(FieldElement):
    def __init__(self, coefficients: Tuple[FieldElement], field=None):
        self.coefficients = coefficients
        self._field = field

    def _create_element(self, coefficients: Iterable[FieldElement]):
        return self._field.create_element(tuple(coefficients))

    def get_field(self):
        return self._field

    def __add__(self, other):
        if other == 0:
            return self
        if not isinstance(other, F32Element):
            raise NotImplementedError()
        result = []
        for i in range(0, len(self.coefficients)):
            result.append(self.coefficients[i] + other.coefficients[i])
        return self._create_element(result)

    @measure
    def __mul__(self, other):
        if isinstance(other, int):
            result = []
            for i in range(0, len(self.coefficients)):
                result.append(self.coefficients[i] * other)
            return self._create_element(result)

        return self._field.get_product(self, other)

    def __neg__(self):
        result = []
        for i in range(0, len(self.coefficients)):
            result.append(-self.coefficients[i])

        return self._create_element(result)

    def __str__(self) -> str:
        result = "%s" % str(self.coefficients[0])
        for i in range(1, len(self.coefficients)):
            result += "+%s𝛿^%d" % (self.coefficients[i], i)

        return result

    @measure
    def __eq__(self, other):
        if not isinstance(other, F32Element):
            return False

        result = True
        for i in range(0, len(self.coefficients)):
            result &= self.coefficients[i] == other.coefficients[i]
        return result

    def __hash__(self):
        return self.coefficients.__hash__()

    def __int__(self):
        result = 0
        for i in range(0, len(self.coefficients)):
            result += int(self.coefficients[i]) * (self._field.base_field.size() ** i)
        return result
    
    @class_property_memorize
    def inverse(self):
        for other in self._field.get_all_elements():
            if self * other == self._field.one():
                return other
        return self._field.zero()

    def norm(self):
        return self._field.base_field.one()

    @class_property_memorize
    def legendre(self) -> int:
        if self == self._field.zero():
            return 0
        for other in self._field.get_all_elements():
            if other * other == self._field.one():
                return 1
        return -1

    def sqrt(self):
        for other in self._field.get_all_elements():
            if other * other == self._field.one():
                return other
        return self._field.zero()

