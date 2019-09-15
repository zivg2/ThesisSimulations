from representations.pgl2.pgl2_character_products_calculator import PGL2CharacterProductsCalculator
from projective_sets.pgl2 import PGL2
from representations import PermutationRepresentation
from group_actions.pgl2_group_action import PGLGroupAction
from group_actions.action_on_tuple import ActionOnTuple

from utilities.general_utilities import get_measure_mapping


def main():
    for q in [3, 5, 7, 9, 11, 13, 17, 19, 23, 25]:
        print('q=%d' % q)
        pgl = PGL2(q)
        action1 = PGLGroupAction(pgl)
        action = ActionOnTuple(action1, 2)
        representation = PermutationRepresentation(action)
        trace_calculations = PGL2CharacterProductsCalculator(pgl)
        decomposition_string = trace_calculations.get_decomposed_representation_string(representation)
        print(str(representation) + '=' + decomposition_string)

    measure_dictionary = get_measure_mapping()
    print("Done!")


if __name__ == "__main__":
    main()
