import networkx as nx
from graphs.oriented_labelled_graph_with_basepoint import OrientedLabelledGraphWithBasePoint
from graphs.graph_from_free_group_factory import GraphFromFreeGroupFactory, CoreGraph
from sympy.combinatorics.free_groups import FreeGroup, FreeGroupElement
from itertools import product, combinations
from typing import Iterable
from utilities.general_utilities import memorize


n = 3
generators_string = ",".join(["a%d" % d for d in range(1, n+1)])

F = FreeGroup(generators_string)
a1, a2, a3 = F.generators

free_group_graph = GraphFromFreeGroupFactory.get_subgroup_core(F.generators)


def get_edge_crosses(graph, element):
    path = graph.get_membership_path(element)
    edge_crosses = {}
    for x in path:
        u, v, n, s = x
        if s.ext_rep[1] < 0:
            u2 = u
            u = v
            v = u2
        generator = s if s.ext_rep[1] > 0 else s.inverse()
        edge_id = (u, v, n, generator)
        if edge_id not in edge_crosses:
            edge_crosses[edge_id] = 0
        edge_crosses[edge_id] += s.ext_rep[1]
    return edge_crosses


def get_all_commutator_foldings(graph, element):
    edge_crosses = get_edge_crosses(graph, element)
    edge_crosses_tuples = [x for x in edge_crosses.items() if x[1] != 0]
    if len(edge_crosses_tuples) == 0:
        return [graph]
    cross1 = edge_crosses_tuples[0]
    edge_crosses_tuples.remove(cross1)
    cross2_list = [x for x in edge_crosses_tuples if x[0][3] == cross1[0][3] and x[1] * cross1[1] < 0]
    foldings = []
    for cross2 in cross2_list:
        new_graph = graph.fold_edge_pair(cross1[0], cross2[0])
        new_graph_foldings = get_all_commutator_foldings(new_graph, element)
        foldings.extend(new_graph_foldings)
    return foldings


def get_commutator_foldings_up_to_isomorphism(graph, element):
    commutator_foldings = get_all_commutator_foldings(graph, element)
    foldings_up_to_isomorphism = []
    for folding in commutator_foldings:
        if all(not folding.is_isomorphic(other_folding) for other_folding in foldings_up_to_isomorphism):
            foldings_up_to_isomorphism.append(folding)
    return foldings_up_to_isomorphism


def is_free_factor(graph: CoreGraph):
    r = 0
    graph_extension = graph.copy()
    while graph_extension.number_of_nodes() > 1:
        r += 1
        labels = [x[3] for x in graph_extension.edges(graph_extension.base_point())
                  if x[1] != graph_extension.base_point()]
        cycle = GraphFromFreeGroupFactory.cycle_from_element(labels[0])
        graph_extension = GraphFromFreeGroupFactory.graph_wedge_sum([graph_extension, cycle])
        graph_extension = graph_extension.fold()
    graph_extension = CoreGraph.from_oriented_labelled_graph_with_base_point(graph_extension)
    d = F.rank - graph_extension.rank()
    return d + r == F.rank - graph.rank()


def get_commutator_foldings_list(a):
    graph = GraphFromFreeGroupFactory.get_subgroup_core([a])
    foldings_up_to_isomorphism = get_commutator_foldings_up_to_isomorphism(graph, a)
    result = [(x, is_free_factor(x)) for x in foldings_up_to_isomorphism]
    return result


def is_in_commutator(graph, element):
    crosses = get_edge_crosses(graph, element)
    return all([x == 0 for x in crosses.values()])


def is_commutator_word(word: FreeGroupElement):
    letters = {s.ext_rep[0]: 0 for s in F.generators}
    for letter in word.letter_form_elm:
        letters[letter.ext_rep[0]] += letter.ext_rep[1]
    values = set(letters.values())
    return values == set() or values == {0}


@memorize
def words_of_len_with_general_ending(k):
    if k == 0:
        return [F.identity]
    elif k == 1:
        return [F.generators[0]]
    elif k == 2:
        return [F.generators[1]*F.generators[0], F.generators[0]*F.generators[0]]
    result = []
    small_words = words_of_len_with_general_ending(k - 1)
    symmetric_generators = list(F.generators)
    symmetric_generators += [x.inverse() for x in F.generators]
    for x, w0 in product(symmetric_generators, small_words):
        if len(w0) == 0 or w0.letter_form_elm[0].ext_rep[0] != x.ext_rep[0] or \
                w0.letter_form_elm[0].ext_rep[1] + x.ext_rep[1] != 0:
            result.append(x*w0)
    return result


def words_of_len_up_to(k):
    if k == 0:
        return words_of_len_with_general_ending(0)
    return words_of_len_up_to(k-1) + words_of_len_with_general_ending(k)


def commutator_candidates_of_len_up_to(k):
    assert(k % 2 == 0)
    if k > 0:
        for w in commutator_candidates_of_len_up_to(k-2):
            yield w
    for w in words_of_len_with_general_ending(k):
        # Up to conjugation
        if len(w) > 1 and w.letter_form_elm[0].ext_rep[0] == F.generators[0].ext_rep[0]:
            continue
        yield w


results = {}
for w in commutator_candidates_of_len_up_to(0):
    if is_commutator_word(w):
        results[w] = get_commutator_foldings_list(w)


def commutator(a: FreeGroupElement, b: FreeGroupElement) -> FreeGroupElement:
    return a.inverse().commutator(b.inverse())


elements = [
    commutator(a1*a1, a2)*commutator(a1, a2),
    commutator(a1*a1, a2)*commutator(a2, a1),

    commutator(a1*a1, a2*a2)*commutator(a1, a2),
    commutator(a1*a1, a2*a2)*commutator(a2, a1),

    commutator(a1*a1, a2)*commutator(a1*a1, a2),
    commutator(a1*a1, a2)*commutator(a2*a2, a1),

    commutator(a1, a2*a2)*commutator(a1, a2),
    commutator(a1, a2*a2)*commutator(a2, a1),

    commutator(a1, a2*a2)*commutator(a1*a1, a2),
    commutator(a1, a2*a2)*commutator(a2*a2, a1),

    commutator(a1, a2*a2)*commutator(a1, a2*a2),
    commutator(a1, a2*a2)*commutator(a2, a1*a1),

    commutator(a1*a1, a2)*commutator(a1, a2*a2),
    commutator(a1*a1, a2)*commutator(a2, a1*a1),

    commutator(a1*a1, a2*a2)*commutator(a1*a1, a2),
    commutator(a1*a1, a2*a2)*commutator(a2*a2, a1),

    commutator(a1*a1, a2*a2)*commutator(a1, a2*a2),
    commutator(a1*a1, a2*a2)*commutator(a2, a1*a1),
]

for element in elements:
    result = get_commutator_foldings_list(element)
    print(element, len(result))
    for r1, r2 in result:
        print(r2)
        r1.draw()
        print()

