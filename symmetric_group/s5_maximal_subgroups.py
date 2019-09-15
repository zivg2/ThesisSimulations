from .sn import SN, SNElement
from itertools import product
from elements_generator import IterableElementsGenerator, ElementsGenerator
from typing import Iterable


def s5_maximal_subgroups() -> Iterable[ElementsGenerator[SNElement]]:
    s5 = SN(5)
    return [alternating_group(s5), point_stabilizer(s5),
            pair_stabilizer(s5), ga_1_5_in_s5(s5)]


def alternating_group(sn: SN):
    return IterableElementsGenerator(
                [element for element in sn.get_all_elements() if element.sign() == 1],
                "A5"
    )


def point_stabilizer(sn: SN):
    i = sn.n - 1
    return IterableElementsGenerator(
                [element for element in sn.get_all_elements() if element[i] == i],
                "S4"
    )


def pair_stabilizer(sn: SN):
    i = sn.n - 1
    j = i - 1
    return IterableElementsGenerator(
                [element for element in sn.get_all_elements() if (element[i] == i and element[j] == j) or
                                                                 (element[i] == j and element[j] == i)],
                "S3*S2"
    )


def ga_1_5_in_s5(sn: SN):
    v5 = sn.create_element([1, 2, 3, 4, 0])
    v4 = sn.create_element([0, 2, 4, 1, 3])
    v5_subgroup = [sn.identity(), v5, v5*v5, v5*v5*v5, v5*v5*v5*v5]
    v4_subgroup = [sn.identity(), v4, v4*v4, v4*v4*v4]
    return IterableElementsGenerator(
                [x*y for x, y in product(v5_subgroup, v4_subgroup)],
                "GA(1, 5)"
    )

