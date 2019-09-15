from abc import ABC, abstractmethod
from typing import List, Iterable
from elements_generator import ElementsGenerator, IterableElementsGenerator


class FiniteGroupAction(ABC):
    @abstractmethod
    def acted_upon_cardinality(self) -> int:
        pass

    @abstractmethod
    def get_acted_upon_elements(self) -> List:
        pass

    @abstractmethod
    def get_acting_elements(self) -> Iterable:
        pass

    def get_elements_generator(self) -> ElementsGenerator:
        return IterableElementsGenerator(self.get_acting_elements())

    @abstractmethod
    def apply(self, g, x):
        pass

    @abstractmethod
    def get_integral_value(self, x):
        pass

