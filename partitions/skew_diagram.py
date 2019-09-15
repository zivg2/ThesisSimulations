from .partition import Partition
from typing import List


class SkewDiagram:
    def __init__(self, outer: Partition, inner: Partition):
        self.outer_partition = outer
        self.inner_partition = inner

    def open_rows_lengths(self) -> List[int]:
        lengths = []
        for i in range(len(self.outer_partition)):
            previous_taken_lines = self.outer_partition[0] if i == 0 else self.inner_partition[i-1]
            j = self.inner_partition[i]
            length_remaining = min(self.outer_partition[i], previous_taken_lines) - j
            lengths.append(length_remaining)
        return lengths

    def print(self):
        for i in range(len(self.outer_partition)):
            line = ""
            for j in range(self.outer_partition[i]):
                if j < self.inner_partition[i]:
                    line += " "
                else:
                    line += "*"
            print(line)

    def __str__(self):
        return "%s-%s" % (self.outer_partition, self.inner_partition)

    def __repr__(self):
        return str(self)