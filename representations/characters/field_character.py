from .character import Character
from fields import FieldMultiplicativeGroup, Field, FieldElement
from numpy import pi, exp


class FieldCharacter(Character):
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def __init__(self, field: Field, i, n):
        self._field_multiplicative_group = FieldMultiplicativeGroup.from_field(field)
        self.i = i
        self.n = n
        self._generator_value = self.get_nth_unity_root(i, n)

    @staticmethod
    def get_nth_unity_root(i, n):
        return exp(2j * pi / n * i)

    def apply(self, x: FieldElement) -> float:
        order = self._field_multiplicative_group.get_power(x)
        return self._generator_value ** order

    def __str__(self):
        return 'ζ%s%s' % (str(self.n).translate(self.SUB), str(self.i).translate(self.SUP))
