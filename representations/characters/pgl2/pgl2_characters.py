from ..trivial_character import TrivialCharacter
from .pgl2_sign_character import PGL2SignCharacter
from ..product_character import ProductCharacter
from .pgl2_standard_character import PGL2StandardCharacter
from .pgl2_diagonalizable_character import PGL2DiagonalizableCharacter
from .pgl2_cuspidal_character import PGL2CuspidalCharacter
from fields import FieldFromInteger, SquareExtensionField
from ..field_character import FieldCharacter

from .. import Character
from typing import List


def get_pgl2q_characters(q) -> List[Character]:
    field = FieldFromInteger.from_q(q)
    sign_character = PGL2SignCharacter()
    standard_character = PGL2StandardCharacter(q)
    characters = []
    characters.extend([
        TrivialCharacter(),
        sign_character,
        standard_character,
        ProductCharacter(standard_character, sign_character),
    ])

    n = q-1
    field_characters = [FieldCharacter(field, i, n) for i in range(1, n//2)]
    normal_diagonalizable_characters = [PGL2DiagonalizableCharacter(q, field_character)
                                        for field_character in field_characters]
    characters.extend(normal_diagonalizable_characters)

    cuspidal_characters = get_pgl2q_cuspidal_characters(q)
    characters.extend(cuspidal_characters)

    return characters


def get_pgl2q_cuspidal_characters(q):
    field = FieldFromInteger.from_q(q)
    square_field = SquareExtensionField.from_base_field(field)
    n2 = q + 1
    square_field_characters = [FieldCharacter(square_field, i, n2) for i in range(1, n2 // 2)]
    cuspidal_characters = [PGL2CuspidalCharacter(q, field_character) for field_character in square_field_characters]
    return cuspidal_characters
