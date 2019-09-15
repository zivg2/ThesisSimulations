from .psl2_character import PSL2Character, PGL2Element
from math import sqrt


class PSL2EvenOscillatorCharacter(PSL2Character):
    def __init__(self, q, sign: int):
        # q is assumed to be 1 mod 4
        self._sign = sign
        super().__init__(q)

    def _apply_on_identity(self) -> float:
        return (self._q + 1) // 2

    def _apply_on_unipotent(self, x: PGL2Element) -> float:
        gamma_sign = self._get_gamma_sign_for_unipotent(x)
        return 0.5 * (1 + self._sign * gamma_sign * sqrt(self._q))

    def _apply_on_diagonalizable(self, x: PGL2Element) -> float:
        ratio = self._get_ratio_for_diagonalizable(x)
        return ratio.legendre()

    def _apply_on_square_diagonalizable(self, x: PGL2Element) -> float:
        return 0

    def __str__(self):
        return 'ωe%s' % ('+' if self._sign == 1 else '-')
