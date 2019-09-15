from .elements_generator import ElementsGenerator, T
from typing import Callable, Iterable, TypeVar
from utilities.general_utilities import class_property_memorize

S = TypeVar("S")


class ActivationElementsGenerator(ElementsGenerator[T]):
    def __init__(self, generator: ElementsGenerator[S], activation: Callable[[S], T]):
        self._generator = generator
        self._activation = activation

    @class_property_memorize
    def get_all_elements(self) -> Iterable[T]:
        elements = self._generator.get_all_elements()
        return [self._activation(x) for x in elements]

    def random_element(self) -> T:
        element = self._generator.random_element()
        return self._activation(element)

    def __str__(self):
        return str(self._activation) + '(' + str(self._generator) + ')'

