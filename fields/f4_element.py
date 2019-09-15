from . import FieldElement
from utilities.general_utilities import class_property_memorize, measure, memorize


class F4Element(FieldElement):
    def __init__(self, x: FieldElement, y: FieldElement = None, field = None):
        self.x = x
        self.y = y
        self._field = field

    def _create_element(self, x: FieldElement, y: FieldElement):
        return self._field.create_element((x, y))

    def get_field(self):
        return self._field

    def __add__(self, other):
        if other == 0:
            return self
        if not isinstance(other, F4Element):
            raise NotImplementedError()
        return self._create_element(self.x + other.x, self.y + other.y)

    @measure
    def __mul__(self, other):
        if isinstance(other, int):
            return self._create_element(
                self.x * other,
                self.y * other
            )

        return self._field.get_product(self, other)

    def __neg__(self):
        return self._create_element(
            -self.x,
            -self.y
        )

    def __str__(self) -> str:
        return str(self.x) + "+" + str(self.y) + '𝛿'

    @measure
    def __eq__(self, other):
        return isinstance(other, F4Element) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __int__(self):
        return int(self.x) + self._field.base_field.size() * int(self.y)
    
    @class_property_memorize
    def inverse(self):
        return self._create_element(
            self.x + self.y,
            self.y
        )

    def norm(self):
        return self._field.base_field.one()

    @class_property_memorize
    def legendre(self) -> int:
        if self == self._field.zero():
            return 0
        if self.y == self._field.base_field.zero():
            return 1
        else:
            return -1

    def conjugate(self):
        return self._create_element(
            self.x + self.y,
            self.y
        )

    def sqrt(self):
        if self.legendre() == 0:
            return self._field.zero()
        elif self.legendre() == -1:
            raise NotImplementedError()
        return self._field.one()

