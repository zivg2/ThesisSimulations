from representations.pgl2 import SignRepresentation, PGL2CuspidalRepresentation, PGL2PrincipalRepresentation
from representations import StandardRepresentation, TensorRepresentation, SumRepresentation
from projective_sets.pgl2 import PGL2
from projective_sets.pgl2_conjugation_classes import pgl2_unipotent_conjugation_class, \
    pgl2_imaginary_roots_conjugation_class, pgl2_diagonal_conjugation_class, pgl2_conjugation_class
from group_actions import PGLGroupAction
import numpy as np
from utilities.primes import odd_primes_up_to

for q in odd_primes_up_to(20):
    print()
    print("q=%d" % q)
    pgl2 = PGL2(q)
    field = pgl2.get_field()
    field_four = field.one() + field.one() + field.one() + field.one()
    conjugation_classes = [[pgl2.create([[field.one(), field.zero()], [field.zero(), field.one()]])],
                           pgl2_unipotent_conjugation_class(q),
                           pgl2_imaginary_roots_conjugation_class(q),
                           pgl2_diagonal_conjugation_class(q)]
    conjugation_classes += [pgl2_conjugation_class(q, s) for s in field.get_all_elements()
                            if s != field.zero() and s != field_four]


    action = PGLGroupAction(pgl2)
    standard_representation = StandardRepresentation(action, pgl2.get_pf().infinity())
    representations = [standard_representation, TensorRepresentation(standard_representation, SignRepresentation())]
    representations += [PGL2PrincipalRepresentation(pgl2, k) for k in range(1, (q - 3)//2 + 1)]
    representations += [PGL2CuspidalRepresentation(pgl2, k) for k in range(1, (q - 1)//2 + 1)]

    permutation_general = SumRepresentation.from_list(representations)
    permutation_general.name = "changed_permutation"

    for conjugation_class in conjugation_classes:

        representations_characters = {representation: representation.get_character().apply(conjugation_class[0]) *
                                                      len(conjugation_class) for representation in representations}
        characters_max = [
            (str(representation),
             np.real(np.round(representations_characters[representation] / representation.dim(), 2)))
            for representation in representations_characters
        ]


        characters_max = sorted(characters_max, key=lambda x: abs(x[1]), reverse=True)

        conjugation_representative = pgl2.get_conjugation_class(conjugation_class[0])
        print(pgl2.get_conjugation_class(conjugation_class[0]), [x for x in characters_max if abs(x[1]) == abs(characters_max[0][1])])

