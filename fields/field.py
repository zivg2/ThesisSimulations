from abc import abstractmethod
from . import FieldElement
from elements_generator import ElementsGenerator
from typing import List


class Field(ElementsGenerator[FieldElement]):
    @abstractmethod
    def create_element(self, x) -> FieldElement:
        pass

    @abstractmethod
    def zero(self) -> FieldElement:
        pass

    @abstractmethod
    def one(self) -> FieldElement:
        pass

    @abstractmethod
    def get_all_elements(self) -> List[FieldElement]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def get_base_element(self, element: FieldElement) -> FieldElement:
        pass

    @abstractmethod
    def trace(self, element: FieldElement) -> FieldElement:
        pass

    @abstractmethod
    def norm(self, element: FieldElement) -> FieldElement:
        pass

    def __str__(self):
        return "F%d" % self.size()
