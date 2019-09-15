import networkx as nx
from networkx.convert_matrix import from_numpy_matrix
import numpy as np
from graph_labelling import UpToConjugationGraphLabelling
from graph_covering.graph_covering import GraphCovering
from graphs.graph_utilities import get_matching_polynomial
from representations import PermutationRepresentation
from projective_sets.pxl2_subsets import *
from group_actions.pgl2_group_action import PGLGroupAction

graph = nx.random_regular_graph(2, 3)
# graph = nx.configuration_model((2,))

q = 7
pgl2 = PGL2(q)
conjugation_classes = pgl2.get_conjugation_classes()

elements_generator = pgl2
action = PGLGroupAction(pgl2)
representation = PermutationRepresentation(action)
up_to_conjugation_elements = pgl2.get_conjugation_classes()
graph_labelling = UpToConjugationGraphLabelling(up_to_conjugation_elements, elements_generator)
graph_covering = GraphCovering(graph, representation)

matching_polynomials = []
matching_polynomials2 = {}
weights = []

for labelling, weight in graph_labelling.weighted_labellings(graph):
    adjacency = graph_covering.adjacency(labelling).astype(int)
    lifted_graph = from_numpy_matrix(adjacency, create_using=nx.MultiGraph, parallel_edges=True)
    polynomial = get_matching_polynomial(lifted_graph)
    matching_polynomials.append(polynomial)
    matching_polynomials2[list(labelling.values())[0]] = polynomial
    weights.append(weight)


average_polynomial = np.average(matching_polynomials, 0, weights)
roots = np.roots(average_polynomial)
roots = np.round(roots, 3)
roots = sorted(roots)
print(list(average_polynomial))
# print(average_polynomial)
print(roots)

print()