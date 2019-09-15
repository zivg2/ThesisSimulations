import networkx as nx

from elements_generator import PermutationsElementsGenerator
from graph_labelling import GraphLabelling
from graph_covering.graph_covering_spectrum import GraphCoveringSpectrum
from representations import TransitiveActionUnitaryStandardRepresentation
from group_actions import SNGroupAction
from utilities.general_utilities import *
from itertools import permutations
from math import factorial


def get_all_graphs(number_of_vertices):
    vertices = list(range(number_of_vertices))
    full_edges = list(combinations(vertices, 2))
    graphs_edges = list(power_set(full_edges))

    graphs = []
    for edges in graphs_edges:
        graph = nx.Graph()
        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)
        graphs.append(graph)

    return graphs


isomorphism_classes = []


def get_isomorphism_class(graph):
    for i, x in enumerate(isomorphism_classes):
        if nx.is_isomorphic(x, graph):
            return i

    isomorphism_classes.append(graph)
    return len(isomorphism_classes) - 1


def get_matching_polynomial_obsolete(adjacency):
    n = adjacency.shape[0]
    polynomial = [1]
    for matching_size in range(2, n+1, 2):
        coefficient = 0
        for possible_matching in permutations(range(n), r=matching_size):
            matching_found = True
            for edge_number in range(0, matching_size, 2):
                i = possible_matching[edge_number]
                j = possible_matching[edge_number + 1]
                if adjacency[i, j] == 0:
                    matching_found = False
                    break
            if matching_found:
                coefficient += 1
        coefficient *= (-1) ** (matching_size//2)
        coefficient //= 2**(matching_size // 2) * factorial(matching_size // 2)
        polynomial.append(0)
        polynomial.append(coefficient)
    return polynomial


@memorize
def _get_matching_polynomial_covering_spectrum():
    elements_generator = PermutationsElementsGenerator(range(2))
    graph_labelling = GraphLabelling(elements_generator)
    action = SNGroupAction(2)
    representation = TransitiveActionUnitaryStandardRepresentation(action, 1)
    return GraphCoveringSpectrum(representation, graph_labelling, 0)


def get_matching_polynomial_by_characteristic(graph):
    graph_covering_spectrum = _get_matching_polynomial_covering_spectrum()
    polynomial = graph_covering_spectrum.return_average_lifts_characteristic_polynomial(graph)
    return np.round(polynomial)


def get_matching_polynomial_recursive(graph):
    if nx.is_empty(graph):
        return np.asarray([1] + [0]*graph.number_of_nodes())
    graph_copy = graph.copy()
    x = list(graph_copy.out_edges)[0]
    graph_copy.remove_edges_from([x])
    edge_removed_matching = get_matching_polynomial_recursive(graph_copy)
    graph_copy.remove_nodes_from([x[0], x[1]])
    vertex_removed_matching = get_matching_polynomial_recursive(graph_copy)
    vertex_removed_matching = np.pad(vertex_removed_matching,
                                     (edge_removed_matching.shape[0] - vertex_removed_matching.shape[0], 0), 'constant')
    return edge_removed_matching - vertex_removed_matching


def get_matching_polynomial(graph: nx.Graph):
    graph_copy = graph.copy()
    graph_copy.remove_edges_from([x for x in graph_copy.edges if x[0] == x[1]])
    return get_matching_polynomial_by_characteristic(graph_copy)
