from . import Field, FieldElement
from utilities.general_utilities import memorize


class FieldMultiplicativeGroup:
    def __init__(self, powers):
        self._powers = powers
        self._inverse_powers = {self._powers[x]: x for x in self._powers}

    @classmethod
    @memorize
    def from_field(cls, field: Field):
        elements = field.get_all_elements()
        elements_number = len(elements)
        for x in elements:
            if x == field.zero():
                continue
            powers = FieldMultiplicativeGroup._create_power_dictionary(x)
            if len(powers) == elements_number - 1:
                return cls(powers)

        raise ValueError()

    @staticmethod
    def _create_power_dictionary(generator: FieldElement):
        field_one = generator.get_field().one()
        power_dictionary = {field_one: 0}
        current_element = generator
        i = 1
        while current_element != field_one:
            power_dictionary[current_element] = i
            current_element *= generator
            i += 1
        return power_dictionary

    def get_power(self, x: FieldElement) -> int:
        return self._powers[x]

    def get_element(self, i):
        return self._inverse_powers[i]
