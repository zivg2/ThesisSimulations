from .partition import Partition
from .kostka_number import kostka_number
from sympy.combinatorics.partitions import IntegerPartition
from utilities.general_utilities import class_property_memorize
import numpy as np
from typing import List


class NPartitions:
    def __init__(self, n):
        self.n = n

    @class_property_memorize
    def get_all_partitions(self) -> List[Partition]:
        partition = IntegerPartition([1] * self.n)
        end_result = IntegerPartition([self.n])
        result = [Partition(partition.partition)]
        while partition != end_result:
            partition = partition.next_lex()
            result.append(Partition(partition.partition))
        return result

    @class_property_memorize
    def kostka_matrix(self):
        partitions = self.get_all_partitions()
        result = []
        for p in partitions:
            result_row = []
            for q in partitions:
                result_row.append(kostka_number(p, q))
            result.append(result_row)
        return np.asarray(result)

    @class_property_memorize
    def inverse_kostka_matrix(self):
        kostka_matrix = self.kostka_matrix()
        result = np.linalg.inv(kostka_matrix)
        result = np.round(result)
        result = result.astype(int)
        return result

    def kostka_number(self, l: Partition, m: Partition):
        matrix = self.kostka_matrix()
        partitions = self.get_all_partitions()
        i = partitions.index(l)
        j = partitions.index(m)
        return matrix[i][j]

    def inverse_kostka_number(self, l: Partition, m: Partition):
        matrix = self.inverse_kostka_matrix()
        partitions = self.get_all_partitions()
        i = partitions.index(l)
        j = partitions.index(m)
        return matrix[i][j]



