from abc import ABC, abstractmethod
from typing import TypeVar, Iterable, Generic
import random

T = TypeVar("T")


class ElementsGenerator(ABC, Generic[T]):
    @abstractmethod
    def get_all_elements(self) -> Iterable[T]:
        pass

    def random_element(self) -> T:
        return random.choice(self.get_all_elements())

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)
