from elements_generator import ElementsGenerator
from .sn_element import SNElement
from typing import Iterable
from partitions import NPartitions

from itertools import permutations


class SN(ElementsGenerator[SNElement]):
    def __init__(self, n):
        self.n = n

    def create_element(self, permutation):
        return SNElement(permutation, self)

    def identity(self):
        return self.create_element([x for x in range(self.n)])

    def get_all_elements(self) -> Iterable[SNElement]:
        return [self.create_element(list(x)) for x in permutations(range(self.n))]

    def __str__(self):
        return "Sym(%d)" % self.n

    def get_all_conjugation_classes(self) -> Iterable[SNElement]:
        result = []
        partitions = NPartitions(self.n)
        for partition in partitions.get_all_partitions():
            permutation = []
            i = 0
            for j in range(len(partition)):
                permutation.extend(range(i+1, partition[j] + i))
                permutation.append(i)
                i += partition[j]
            result.append(self.create_element(permutation))
        return result
