from .elements_generator import ElementsGenerator, T
from typing import Callable, Iterable
from utilities.general_utilities import class_property_memorize


class ConditionalElementsGenerator(ElementsGenerator):
    def __init__(self, generator: ElementsGenerator[T], condition: Callable[[T], bool]):
        self._generator = generator
        self._condition = condition

    @class_property_memorize
    def get_all_elements(self) -> Iterable[T]:
        elements = self._generator.get_all_elements()
        return [x for x in elements if self._condition(x)]

    def random_element(self) -> T:
        finished = False
        element = None
        while not finished:
            element = self._generator.random_element()
            finished = self._condition(element)
        return element

    def __str__(self):
        return str(self._generator) + ' if ' + str(self._condition)

