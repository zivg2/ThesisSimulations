from .elements_generator import ElementsGenerator, T
from typing import Iterable, Generic
from utilities.general_utilities import class_property_memorize
import random


class IterableElementsGenerator(ElementsGenerator[T], Generic[T]):
    def __init__(self, iterable: Iterable[T], name: str=None):
        self._iterable = iterable
        self._name = name

    @class_property_memorize
    def get_all_elements(self) -> Iterable[T]:
        return self._iterable

    def random_element(self) -> T:
        return random.choice(self._iterable)

    def __str__(self):
        if self._name is None:
            return str(self._iterable)
        else:
            return self._name

