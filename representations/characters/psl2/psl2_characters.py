from ..trivial_character import TrivialCharacter
from .psl2_standard_character import PSL2StandardCharacter
from .psl2_diagonalizable_character import PSL2DiagonalizableCharacter
from .psl2_cuspidal_character import PSL2CuspidalCharacter
from .psl2_even_oscillator_character import PSL2EvenOscillatorCharacter
from .psl2_odd_oscillator_character import PSL2OddOscillatorCharacter
from fields import FieldFromInteger, SquareExtensionField
from ..field_character import FieldCharacter

from .. import Character
from typing import List


def get_psl2q_characters(q) -> List[Character]:
    field = FieldFromInteger.from_q(q)
    standard_character = PSL2StandardCharacter(q)

    characters = list()
    characters.append(TrivialCharacter())
    characters.append(standard_character)

    n = q-1
    field_characters = [FieldCharacter(field, i, n) for i in range(2, n//2, 2)]
    normal_diagonalizable_characters = [PSL2DiagonalizableCharacter(q, field_character)
                                        for field_character in field_characters]
    characters.extend(normal_diagonalizable_characters)

    square_field = SquareExtensionField.from_base_field(field)
    n2 = q+1
    square_field_characters = [FieldCharacter(square_field, i, n2) for i in range(1, (n2//2+1)//2)]
    cuspidal_characters = [PSL2CuspidalCharacter(q, field_character)
                                        for field_character in square_field_characters]
    characters.extend(cuspidal_characters)

    if q % 4 == 1:
        oscillator_class = PSL2EvenOscillatorCharacter
    else:
        oscillator_class = PSL2OddOscillatorCharacter

    characters.append(oscillator_class(q, 1))
    characters.append(oscillator_class(q, -1))

    return characters
