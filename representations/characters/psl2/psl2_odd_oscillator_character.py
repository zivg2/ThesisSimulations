from .psl2_character import PSL2Character, PGL2Element
from ..field_character import FieldCharacter
from math import sqrt


class PSL2OddOscillatorCharacter(PSL2Character):
    def __init__(self, q, sign: int):
        # q is assumed to be 3 mod 4
        self._sign = sign
        super().__init__(q)
        self._chi0 = FieldCharacter(self._square_extension, (q+1)//4, q+1)

    def _apply_on_identity(self) -> float:
        return (self._q - 1) // 2

    def _apply_on_unipotent(self, x: PGL2Element) -> float:
        gamma_sign = self._get_gamma_sign_for_unipotent(x)
        return 0.5 * (-1 + self._sign * gamma_sign * sqrt(self._q) * 1.0j)

    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        return 0

    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        z = self._get_z_for_square_diagonalizable(x)
        res = self._chi0.apply(z)
        return -res

    def __str__(self):
        return 'ωo%s' % ('+' if self._sign == 1 else '-')
