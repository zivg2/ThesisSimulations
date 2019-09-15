import numpy as np

from projective_sets.pgl2 import PGL2
from representations import get_pgl2q_characters, Character, Representation
from utilities.general_utilities import measure, round_up_to


class PGL2CharacterProductsCalculator:
    @measure
    def __init__(self, pgl: PGL2):
        self.q = pgl.q()
        self.conjugation_classes = pgl.get_conjugation_classes()
        self.characters = get_pgl2q_characters(self.q)
        self.elements = pgl.get_all_elements()

    def get_product(self, chi1: Character, chi2: Character):
        result = self.get_value_sum(chi1, chi2)
        result = round_up_to(result)
        if np.imag(result) != 0:
            raise ValueError()
        result = np.real(result)
        result /= len(self.elements)
        result = round_up_to(result)
        if result != int(result):
            raise ValueError()
        result = int(result)
        return result

    def get_value_sum(self, chi1: Character, chi2: Character):
        products = [chi1.apply(element) * np.conj(chi2.apply(element)) *
                    self.conjugation_classes[element] for element in self.conjugation_classes]
        return sum(products)

    @measure
    def decompose_representation(self, representation: Representation):
        chi = representation.get_character()
        character_products = {character: self.get_product(chi, character) for character in self.characters}
        return character_products

    @measure
    def get_decomposed_representation_string(self, representation):
        character_products = self.decompose_representation(representation)
        summands_string = self.get_summands_string(character_products)
        return '+'.join(summands_string)

    @staticmethod
    def get_summands_string(character_products):
        summands_string = [PGL2CharacterProductsCalculator.get_summand_string(character_products[x], x)
                           for x in character_products if character_products[x] != 0]
        return summands_string

    @staticmethod
    def get_summand_string(quantity, representation):
        representation_string = str(representation)
        representation_string = representation_string.replace('χ_', '')
        representation_string = representation_string.replace('std*sgn', '^std')
        if quantity == 1:
            return '%s' % representation_string
        else:
            return "%s%s" % (quantity, representation_string)
