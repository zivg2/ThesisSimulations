from utilities.general_utilities import measure, class_property_memorize
from .pgl2_group_action import PGLGroupAction
from elements_generator.elements_generator import ElementsGenerator


class StabilizedPGLGroupAction(PGLGroupAction):
    def __init__(self, pgl, stabilized_elements, stabilizer_generator: ElementsGenerator):
        super().__init__(pgl)
        self.stabilized_elements = stabilized_elements
        self.stabilizer_generator = stabilizer_generator

    def acted_upon_cardinality(self) -> int:
        return self._pgl.q() + 1 - len(self.stabilized_elements)

    @class_property_memorize
    def get_acted_upon_elements(self):
        return [x for x in self._pf.get_all_elements() if x not in self.stabilized_elements]

    def get_acting_elements(self):
        return self.stabilizer_generator.get_all_elements()

    @class_property_memorize
    def _stabilized_elements_integral_values(self):
        integral_value_function = super().get_integral_value
        result = [integral_value_function(x) for x in self.stabilized_elements]
        return sorted(result)

    @measure
    def get_integral_value(self, x):
        result = super().get_integral_value(x)
        diff = 0
        for i in self._stabilized_elements_integral_values():
            if result > i:
                diff += 1
        result -= diff
        return result
