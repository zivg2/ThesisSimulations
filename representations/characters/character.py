from abc import ABC, abstractmethod


class Character(ABC):
    @abstractmethod
    def apply(self, x) -> float:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)
