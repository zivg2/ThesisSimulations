from .pgl2_character import PGL2Character, PGL2Element
from ..field_character import FieldCharacter


class PGL2DiagonalizableCharacter(PGL2Character):
    def __init__(self, q, base_field_character: FieldCharacter):
        self._base_field_character = base_field_character
        super().__init__(q)

    def _apply_on_identity(self) -> float:
        return self._q + 1

    def _apply_on_unipotent(self) -> float:
        return 1

    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        ratio = self._get_ratio_for_diagonalizable(x)
        return self._base_field_character.apply(ratio) + self._base_field_character.apply(ratio) ** (-1)

    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        return 0

    def __str__(self):
        return 'ρ%s' % str(self._base_field_character.i)
