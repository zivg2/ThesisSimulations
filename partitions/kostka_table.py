from partitions import Partition
from .n_partitions import NPartitions
from typing import List

IntMatrix = List[List[int]]


raw_tables = [
    ([],
     [],
     [],),

    ([[1]],
     [[1]],
     [[1]],),

    ([[1, 1], [2]],
     [[1, 0],
      [1, 1]],
     [[1, 0],
      [-1, 1]],),

    ([[1, 1, 1], [2, 1], [3]],
     [[1, 0, 0],
      [2, 1, 0],
      [1, 1, 1]],
     [[1, 0, 0],
      [-2, 1, 0],
      [1, -1, 1]],),

    ([[1, 1, 1, 1], [2, 1, 1], [2, 2], [3, 1], [4]],
     [[1, 0, 0, 0, 0],
      [3, 1, 0, 0, 0],
      [2, 1, 1, 0, 0],
      [3, 2, 1, 1, 0],
      [1, 1, 1, 1, 1]],
     [[1, 0, 0, 0, 0],
      [-3, 1, 0, 0, 0],
      [1, -1, 1, 0, 0],
      [2, -1, -1, 1, 0],
      [-1, 1, 0, -1, 1]],),

    ([[1, 1, 1, 1, 1], [2, 1, 1, 1], [2, 2, 1], [3, 1, 1], [3, 2], [4, 1], [5]],
     [[1, 0, 0, 0, 0, 0, 0],
      [4, 1, 0, 0, 0, 0, 0],
      [5, 2, 1, 0, 0, 0, 0],
      [6, 3, 1, 1, 0, 0, 0],
      [5, 3, 2, 1, 1, 0, 0],
      [4, 3, 2, 2, 1, 1, 0],
      [1, 1, 1, 1, 1, 1, 1]],
     [[1, 0, 0, 0, 0, 0, 0],
      [-4, 1, 0, 0, 0, 0, 0],
      [3, -2, 1, 0, 0, 0, 0],
      [3, -1, -1, 1, 0, 0, 0],
      [-2, 2, -1, -1, 1, 0, 0],
      [-2, 1, 1, -1, -1, 1, 0],
      [1, -1, 0, 1, 0, -1, 1]],)
]


class KostkaTable:
    @classmethod
    def from_raw_table(cls, raw_table):
        partitions = [Partition(x) for x in raw_table[0]]
        kostka_table = raw_table[1]
        inverse_kostka_table = raw_table[2]
        return cls(partitions, kostka_table, inverse_kostka_table)

    @classmethod
    def calculate(cls, n):
        partitions_generator = NPartitions(n)
        return cls(
            partitions_generator.get_all_partitions(),
            partitions_generator.kostka_matrix(),
            partitions_generator.inverse_kostka_matrix()
                )

    def __init__(self, partitions: List[Partition],
                 kostka_table: IntMatrix, inverse_kostka_table: IntMatrix):
        self.partitions = partitions
        self._kostka_table = kostka_table
        self._inverse_kostka_table = inverse_kostka_table

    def kostka(self, shape: Partition, content: Partition):
        i = self.partitions.index(shape)
        j = self.partitions.index(content)
        return self._kostka_table[i][j]

    def inverse_kostka(self, shape: Partition, content: Partition):
        i = self.partitions.index(shape)
        j = self.partitions.index(content)
        return self._inverse_kostka_table[i][j]


def get_tables(up_to_n):
    tables = [KostkaTable([], [], [])]
    tables += [KostkaTable.calculate(n) for n in range(1, up_to_n + 1)]
    return tables
