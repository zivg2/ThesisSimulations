from . import FieldElement
from utilities.general_utilities import class_property_memorize, measure, memorize


class SquareExtensionFieldElement(FieldElement):
    def __init__(self, x: FieldElement, y: FieldElement=None, field=None):
        self.x = x
        self.y = y
        self._field = field

    def _create_element(self, x: FieldElement, y: FieldElement):
        return self._field.create_element((x, y))

    def get_field(self):
        return self._field

    def __add__(self, other):
        if not isinstance(other, SquareExtensionFieldElement):
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
        return isinstance(other, SquareExtensionFieldElement) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __int__(self):
        return int(self.x) + self._field.base_field.size() * int(self.y)
    
    @class_property_memorize
    def inverse(self):
        denominator = self.norm()
        return self._create_element(
            self.x / denominator,
            -self.y / denominator
        )

    def norm(self):
        return self.x * self.x - self._field.non_square_element * self.y * self.y

    @class_property_memorize
    def legendre(self) -> int:
        if self == self._field.zero():
            return 0
        if self.y == self._field.base_field.zero():
            return 1

        discriminant = self.norm()
        if discriminant.legendre() == -1:
            return -1

        discriminant_sqrt = discriminant.sqrt()
        x_square1 = (self.x + discriminant_sqrt) / self._field.base_field.create_element(2)
        x_square2 = (self.x - discriminant_sqrt) / self._field.base_field.create_element(2)

        if x_square1.legendre() == -1 and x_square2.legendre() == -1:
            return -1

        return 1

    def conjugate(self):
        return self._create_element(
            self.x,
            -self.y
        )

    def sqrt(self):
        if self.legendre() == 0:
            return self._field.zero()
        elif self.legendre() == -1:
            raise NotImplementedError()

        if self.y == self._field.base_field.zero():
            if self.x.legendre() == 1:
                return self._field.create_element(
                    (self.x.sqrt(), self._field.base_field.zero())
                )
            else:
                return self._field.create_element(
                    (self._field.base_field.zero(), (self.x / self._field.non_square_element).sqrt())
                )

        discriminant = self.norm()
        discriminant_sqrt = discriminant.sqrt()
        x_square = (self.x + discriminant_sqrt) / self._field.create_element(2)
        if x_square.legendre() >= 0:
            x = x_square.sqrt()
        else:
            x_square = (self.x - discriminant_sqrt) / self._field.create_element(2)
            x = x_square.sqrt()
        y = self.y / (2*x)
        return self._field.create_element((x, y))

