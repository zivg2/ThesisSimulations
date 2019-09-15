from projective_sets.pgl2 import PGL
from fields import SquareExtensionField
from representations.characters.pgl2.pgl2_characters import get_pgl2q_characters
from representations.characters.pgl2.pgl2_cuspidal_character import PGL2CuspidalCharacter
from itertools import product
from numpy import real


q = 3
pgl2 = PGL(2, q)
field = pgl2.get_field()
delta = SquareExtensionField.get_non_square_element(field)

group = [pgl2.create([[a, delta*b],[b, a]]) for a, b in product(field.get_all_elements(), repeat=2)
         if a != field.zero() or b != field.zero()]

group += [pgl2.create([[a, -delta*b],[b, -a]]) for a, b in product(field.get_all_elements(), repeat=2)
         if a != field.zero() or b != field.zero()]

for character in get_pgl2q_characters(q):
    s = round(sum(character.apply(x) for x in group)) / len(group)
    s = real(s)
    print(character, s)
