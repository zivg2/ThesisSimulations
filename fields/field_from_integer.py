from .field import Field
from .prime_field import PrimeField
from .f4 import F4
from .f32 import F32
from utilities.general_utilities import memorize
from .square_extension_field import SquareExtensionField

from sympy import isprime


class FieldFromInteger:
    @staticmethod
    @memorize
    def from_q(q) -> Field:
        if isprime(q):
            return PrimeField(q)
        if q == 4:
            return F4()
        if q == 32:
            return F32()
        p = int(q ** 0.5)
        if p*p == q:
            return SquareExtensionField.from_base_field(FieldFromInteger.from_q(p))
        else:
            raise NotImplementedError()
