from .psl2_character import PSL2Character, PGL2Element
from ..field_character import FieldCharacter


class PSL2CuspidalCharacter(PSL2Character):
    def __init__(self, q, square_field_character: FieldCharacter):
        self._square_field_character = square_field_character
        super().__init__(q)

    def _apply_on_identity(self) -> float:
        return self._q - 1

    def _apply_on_unipotent(self, x: PGL2Element) -> float:
        return -1

    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        return 0

    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        z = self._get_z_for_square_diagonalizable(x)
        return -(self._square_field_character.apply(z) + self._square_field_character.apply(z)**(-1))

    def __str__(self):
        return 'π%s' % str(self._square_field_character.i)
