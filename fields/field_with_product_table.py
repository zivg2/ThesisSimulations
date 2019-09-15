from abc import abstractmethod
from . import FieldElement, Field
from utilities.general_utilities import class_property_memorize


class FieldWithProductTable(Field):
    @abstractmethod
    def get_product(self, a, b) -> FieldElement:
        pass

    @class_property_memorize
    def get_squares_dictionary(self):
        return {x: self.get_product(x, x) for x in self.get_all_elements()}
