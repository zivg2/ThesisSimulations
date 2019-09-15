from .elements_generator import ElementsGenerator, T
from typing import Callable, Iterable, TypeVar, Tuple
from utilities.general_utilities import class_property_memorize
from itertools import product

S = TypeVar("S")


class ProductElementsGenerator(ElementsGenerator[Tuple[S, T]]):
    def __init__(self, generator1: ElementsGenerator[S], generator2: ElementsGenerator[T]):
        self._generator1 = generator1
        self._generator2 = generator2

    @class_property_memorize
    def get_all_elements(self) -> Iterable[Tuple[S, T]]:
        return product(self._generator1.get_all_elements(), self._generator2.get_all_elements())

    def random_element(self) -> Tuple[S, T]:
        element1 = self._generator1.random_element()
        element2 = self._generator2.random_element()
        return element1, element2

    def __str__(self):
        return str(self._generator1) + "*" + str(self._generator2)

