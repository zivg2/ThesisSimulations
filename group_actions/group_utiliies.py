from utilities.general_utilities import memorize
from group_actions.finite_group_action import FiniteGroupAction
import math, scipy.misc
from typing import List, TypeVar, Callable
from elements_generator import ElementsGenerator

T = TypeVar("T")

@memorize
def permutation_parity(permutation: list):
    permutation = list(permutation)
    parity = 1
    for i in range(0, len(permutation)-1):
        if permutation[i] != i:
            parity *= -1
            min_value = min(range(i, len(permutation)), key=permutation.__getitem__)
            permutation[i], permutation[min_value] = permutation[min_value], permutation[i]
    return parity


def is_action_transitive(action: FiniteGroupAction, acting_element):
    acted_upon_elements = action.get_acted_upon_elements()
    first_element = acted_upon_elements[0]
    element = action.apply(acting_element, first_element)
    i = 1
    while element != first_element:
        i += 1
        element = action.apply(acting_element, element)

    return i == len(acted_upon_elements)


def get_n_partitions(n):
    def get_n_partitions_smaller_than_k(n, k, start):
        if n == 0:
            return [start]
        if k == 0:
            return []
        new_partitions = []
        if n >= k:
            new_partitions.extend(get_n_partitions_smaller_than_k(n-k, k, start + [k]))
        if k > 0:
            new_partitions.extend(get_n_partitions_smaller_than_k(n, k-1, start))
        return new_partitions
    return get_n_partitions_smaller_than_k(n, n, [])


def get_partition_representative(partition):
    last_x = 0
    result = []
    for i in partition:
        result.extend((t + 1) % i + last_x for t in range(i))
        last_x += i
    return tuple(result)


def get_partition_amount(n, partition):
    result = math.factorial(n)
    last_i = 0
    number_of_is = 0
    for i in partition:
        if i == last_i:
            number_of_is += 1
        else:
            number_of_is = 1
        result //= (i * number_of_is)
        last_i = i
    return result


@memorize
def get_sn_conjugation_classes(n):
    partitions = get_n_partitions(n)
    result = {}
    for partition in partitions:
        representative = get_partition_representative(partition)
        amount = get_partition_amount(n, partition)
        result[representative] = amount
    return result


def get_extension_of_order_2(group_elements: List[T],
                             super_group: ElementsGenerator[T],
                             extending_element_condition: Callable[[T], bool]):
    conjugation_candidates = super_group.get_all_elements()
    conjugation_candidates = set(x for x in conjugation_candidates if extending_element_condition(x))
    for x in group_elements:
        if x in conjugation_candidates:
            conjugation_candidates.remove(x)
    while len(conjugation_candidates) > 0:
        g = conjugation_candidates.pop()
        conjugated = {g * x * g.inverse() for x in group_elements}
        if conjugated == group_elements:
            extension = [x for x in group_elements]
            extension += [g * x for x in group_elements]
            return extension
        for x in group_elements:
            if g*x in conjugation_candidates:
                conjugation_candidates.remove(g * x)
    return group_elements

