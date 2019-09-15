from .pgl2_character import PGL2Character, PGL2Element


class PGL2StandardCharacter(PGL2Character):
    def _apply_on_identity(self) -> float:
        return self._q

    def _apply_on_unipotent(self) -> float:
        return 0

    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        return 1

    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        return -1

    def __str__(self):
        return 'χ_std'
