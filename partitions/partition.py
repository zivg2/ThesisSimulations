from .composition import Composition
from .schur_polynomial import schur_polynomial
from utilities.general_utilities import class_property_memorize


class Partition(Composition):
    @classmethod
    def from_composition(cls, composition: Composition):
        return cls(composition.sequence)
        
    def __init__(self, sequence):
        sorted_sequence = sorted(sequence, reverse=True)
        super().__init__(sorted_sequence)

    def dominates(self, other):
        s = 0
        for i in range(min(len(self), len(other))):
            s += self[i] - other[i]
            if s < 0:
                return False
        return True

    def lexicographic_smaller(self, other):
        for i in range(max(len(self), len(other))):
            if self[i] < other[i]:
                return True
            elif self[i] > other[i]:
                return False
        return True

    def union(self, other):
        composition = super().union(other)
        return Partition(composition.sequence)

    def __add__(self, other):
        composition = super().__add__(other)
        return Partition(composition.sequence)

    def __lt__(self, other):
        return self.lexicographic_smaller(other)

    @class_property_memorize
    def schur_polynomial(self):
        return schur_polynomial(self.padded_sequence(self.n()))

    @class_property_memorize
    def conjugate(self):
        j = 1
        temp_arr = list(self.sequence) + [0]
        k = temp_arr[0]
        b = [0] * k
        while k > 0:
            while k > temp_arr[j]:
                b[k - 1] = j
                k -= 1
            j += 1
        return Partition(b)

    def n_lambda(self):
        return sum([i*self[i] for i in range(len(self))])


