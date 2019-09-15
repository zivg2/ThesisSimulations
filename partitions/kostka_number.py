from .partition import Partition
from .composition import Composition
from .skew_diagram import SkewDiagram
from utilities.general_utilities import memorize
from typing import Tuple, List
from sympy.combinatorics.partitions import IntegerPartition

IntTuple = Tuple[int, ...]


@memorize
def kostka_number(shape: Partition, content: Composition):
    return kostka_by_skew_diagram(shape, content)


def kostka_number_by_schur_polynomial(shape, content):
    s = shape.schur_polynomial()
    s_dictionary = s.as_dict()
    other_sequence = content.padded_sequence(shape.n())
    result = s_dictionary[other_sequence] if other_sequence in s_dictionary else 0
    return int(result)


def _get_all_partitions_tuples(n) -> List[IntTuple]:
    partition = IntegerPartition([1] * n)
    end_result = IntegerPartition([n])
    result = [tuple(partition.partition)]
    while partition != end_result:
        partition = partition.next_lex()
        result.append(tuple(partition.partition))
    return result


def kostka_by_skew_diagram(shape: Partition, content: Composition):
    diagram = SkewDiagram(shape, Partition([0]))
    return kostka_of_skew_diagram(diagram, tuple(content.sequence))


@memorize
def kostka_of_skew_diagram(shape: SkewDiagram, content: IntTuple):
    if len(content) == 0:
        return 1
    result = 0
    open_row_lengths = shape.open_rows_lengths()
    sub_compositions = Composition.sub_compositions(open_row_lengths, content[0])
    for composition in sub_compositions:
        sub_composition = Partition.from_composition(shape.inner_partition + composition)
        diagram = SkewDiagram(shape.outer_partition, sub_composition)
        s = kostka_of_skew_diagram(diagram, content[1:])
        result += s
    return result


