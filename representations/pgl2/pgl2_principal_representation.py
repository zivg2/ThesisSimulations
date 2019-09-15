from representations import Representation, Character
from representations.characters.field_character import FieldCharacter
from representations.characters.pgl2.pgl2_diagonalizable_character import PGL2DiagonalizableCharacter
from group_actions import PGLGroupAction
import numpy as np


class PGL2PrincipalRepresentation(Representation):
    def __init__(self, pgl2, k):
        self._pgl2 = pgl2
        self._pf2 = pgl2.get_pf()
        self._action = PGLGroupAction(pgl2)
        self._q = pgl2.q()
        self._base_character = FieldCharacter(self._pgl2.get_field(), k, self._q - 1)

    def apply(self, g) -> np.ndarray:
        result = np.zeros((self.dim(), self.dim()), dtype=complex)
        infinity = self._pf2.infinity()
        g2 = self._pgl2.create([[g.d, g.c], [g.b, g.a]])
        for x in self._action.get_acted_upon_elements():
            x2 = self._pf2.create([x[1], x[0]])
            y2 = self._action.apply(g2, x2)
            y = self._pf2.create([y2[1], y2[0]])
            s = g.a + g.b * x[1]/x[0] if x[0] != 0 else g.b
            if y2 != infinity:
                value = self._base_character.apply(s * s / g.det())
            else:
                if x2 != infinity:
                    value = self._base_character.apply(g.det() / (g.b * g.b))
                else:
                    value = self._base_character.apply(g.d/g.a)

            i = self._action.get_integral_value(x)
            j = self._action.get_integral_value(y)
            result[i, j] = value
        return result

    def dim(self) -> int:
        return self._q+1

    def get_character(self) -> Character:
        return PGL2DiagonalizableCharacter(self._q, self._base_character)

    def __str__(self):
        return 'ρ%s' % str(self._base_character.i)
