from utilities.general_utilities import class_property_memorize, measure
from . import FieldElement
from .field_with_product_table import FieldWithProductTable
from fields.prime_field_utilities import extended_euclidean_algorithm, fast_power


class PrimeFieldElement(FieldElement):
    def __init__(self, n: int, p: int, field: FieldWithProductTable):
        self.n = n % p
        self._p = p
        self._field = field

    def get_field(self):
        return self._field

    def __add__(self, other):
        if not isinstance(other, PrimeFieldElement):
            return self + self._field.create_element(other)
        return self._field.create_element(self.n + other.n)

    @measure
    def __sub__(self, other):
        if not isinstance(other, PrimeFieldElement):
            return self - self._field.create_element(other)

        return self._field.create_element(self.n - other.n)

    @measure
    def __mul__(self, other):
        if not isinstance(other, PrimeFieldElement):
            return self * self._field.create_element(other)
        return self._field.get_product(self, other)

    def __neg__(self):
        return self._field.create_element(-self.n)

    @measure
    def __eq__(self, other):
        return (isinstance(other, PrimeFieldElement) and self.n == other.n) or \
               (isinstance(other, int) and self.n == other)

    def __hash__(self):
        return (self.n, self._p).__hash__()

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return '%d (mod %d)' % (self.n, self._p)

    def __int__(self):
        return self.n

    @class_property_memorize
    def inverse(self):
        if self.n == 0:
            raise ZeroDivisionError()
        x, y, d = extended_euclidean_algorithm(self.n, self._p)
        return PrimeFieldElement(x, self._p, self._field)

    @class_property_memorize
    def legendre(self) -> int:
        sign_in_field = PrimeFieldElement(fast_power(self.n, (self._p - 1) // 2), self._p, self._field)
        if sign_in_field == self._field.one():
            return 1
        elif sign_in_field == -self._field.one():
            return -1
        else:
            return 0

    @class_property_memorize
    def sqrt(self):
        if self.legendre() == 0:
            return self._field.zero()
        elif self.legendre() == -1:
            raise NotImplementedError()
        squares = self._field.get_squares_dictionary()

        return next(x for x in squares if squares[x] == self)
