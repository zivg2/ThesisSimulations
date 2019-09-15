from abc import ABC, abstractmethod


class FieldElement(ABC):
    @abstractmethod
    def get_field(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def legendre(self) -> int:
        pass

    @abstractmethod
    def sqrt(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __int__(self):
        pass

    def __repr__(self) -> str:
        return str(self)

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * other.inverse()

    def __div__(self, other):
        return self * other.inverse()

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        if self == self.get_field().zero():
            return self
        if power == 0:
            return self.get_field().one()
        elif power % 2 == 1:
            return self * (self ** (power - 1))
        return (self ** (power // 2)) * (self ** (power // 2))
