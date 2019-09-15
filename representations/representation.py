from abc import ABC, abstractmethod
import numpy as np
from .characters import Character


class Representation(ABC):
    @abstractmethod
    def apply(self, x) -> np.ndarray:
        pass

    def apply_up_to_conjugation(self, x) -> np.ndarray:
        return self.apply(x)

    @abstractmethod
    def dim(self) -> int:
        pass

    @abstractmethod
    def get_character(self) -> Character:
        pass

    @abstractmethod
    def __str__(self):
        pass
