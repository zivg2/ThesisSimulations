from abc import abstractmethod

from representations.characters.character import Character
from projective_sets.pgl2_element import PGL2Element
from fields import SquareExtensionField, FieldFromInteger


class PSL2Character(Character):
    def __init__(self, q):
        self._base_field = FieldFromInteger.from_q(q)
        self._q = q
        self._square_extension = SquareExtensionField.from_base_field(self._base_field)

    def apply(self, x: PGL2Element) -> float:
        discriminant = self._get_discriminant(x)
        is_square = discriminant.legendre()
        if is_square == 0:
            if x.b == self._base_field.zero() and x.c == self._base_field.zero():
                return self._apply_on_identity()
            else:
                return self._apply_on_unipotent(x)
        elif is_square == 1:
            return self._apply_on_diagonalizable(x)
        else:
            return self._apply_on_square_diagonalizable(x)

    @staticmethod
    def _get_discriminant(x: PGL2Element):
        return x.trace() * x.trace() - 4 * x.det()

    @abstractmethod
    def _apply_on_identity(self) -> float:
        # 1, 0
        # 0, 1
        pass

    @abstractmethod
    def _apply_on_unipotent(self, x: PGL2Element) -> float:
        # 1, x
        # 0, 1
        # x is 1 or non-square
        pass

    @staticmethod
    def _get_gamma_sign_for_unipotent(x: PGL2Element):
        field_two = x.field.one() + x.field.one()
        return (field_two * x.trace() * x.b).legendre()

    @abstractmethod
    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        # x, 0
        # 0, x**(-1)
        pass

    @staticmethod
    def _get_ratio_for_diagonalizable(x: PGL2Element):
        discriminant = PSL2Character._get_discriminant(x)
        discriminant_sqrt = discriminant.sqrt()
        determinant_sqrt = x.det().sqrt()
        field_two = x.field.one() + x.field.one()
        ratio = (x.trace() + discriminant_sqrt) / (field_two * determinant_sqrt)
        return ratio

    @abstractmethod
    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        # x, delta*y
        # y, x
        pass

    def _get_z_for_square_diagonalizable(self, x: PGL2Element):
        # x, delta*y
        # y, x
        # z = x + sqrt(delta)*y
        discriminant = self._get_discriminant(x)
        discriminant_sqrt = self._square_extension.from_base_field_element(discriminant).sqrt()
        z_base = self._square_extension.from_base_field_element(x.trace())
        field_two = self._square_extension.one() + self._square_extension.one()
        z = (z_base + discriminant_sqrt) / field_two
        return z

    @abstractmethod
    def __str__(self):
        super().__str__()