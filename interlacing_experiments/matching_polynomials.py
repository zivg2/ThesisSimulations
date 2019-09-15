import networkx as nx
from networkx.convert_matrix import from_numpy_matrix
import numpy as np
import scipy.linalg as linalg
from graph_labelling import UpToConjugationGraphLabelling
from graph_covering.graph_covering import GraphCovering
from graphs.graph_utilities import get_matching_polynomial
from representations import PermutationRepresentation, TransitiveActionUnitaryStandardRepresentation
from projective_sets.pxl2_subsets import *
from group_actions.pgl2_group_action import PGLGroupAction
from group_actions.stabilized_pgl2_group_action import StabilizedPGLGroupAction
from elements_generator.iterable_elements_generator import IterableElementsGenerator

# graph = nx.random_regular_graph(2, 3)
graph = nx.configuration_model((2,))

q = 3
pgl2 = PGL2(q)
conjugation_classes = pgl2.get_conjugation_classes()

triangular_subset = pgl2_upper_triangular(q)

elements_generator = IterableElementsGenerator(triangular_subset)
projective_zero = pgl2.get_pf().zero()
projective_infinity = pgl2.get_pf().infinity()
action = StabilizedPGLGroupAction(pgl2, [projective_zero], elements_generator)
representation = PermutationRepresentation(action)
up_to_conjugation_elements = {}
for element in triangular_subset:
    conjugation_class = pgl2.get_conjugation_class(element)
    if conjugation_class not in up_to_conjugation_elements:
        up_to_conjugation_elements[conjugation_class] = 0
    up_to_conjugation_elements[conjugation_class] += 1
graph_labelling = UpToConjugationGraphLabelling(up_to_conjugation_elements, elements_generator)
graph_covering = GraphCovering(graph, representation)

action2 = PGLGroupAction(pgl2)
representation2 = TransitiveActionUnitaryStandardRepresentation(action2, pgl2.get_pf().infinity())
graph_labelling2 = UpToConjugationGraphLabelling(conjugation_classes, pgl2)
graph_covering2 = GraphCovering(graph, representation2)

characteristic_polynomials = []
characteristic_weights = []
matching_polynomials = []
matching_polynomials2 = {}
characteristic_polynomials2 = {}
weights = []

for labelling, weight in graph_labelling.weighted_labellings(graph):
    adjacency = graph_covering.adjacency(labelling).astype(int)
    lifted_graph = from_numpy_matrix(adjacency, create_using=nx.MultiGraph, parallel_edges=True)
    polynomial = get_matching_polynomial(lifted_graph)
    matching_polynomials.append(polynomial)
    matching_polynomials2[list(labelling.values())[0]] = polynomial
    weights.append(weight)

for labelling, weight in graph_labelling2.weighted_labellings(graph):
    polynomial = graph_covering2.get_polynomial(labelling)
    characteristic_polynomials.append(polynomial)
    characteristic_polynomials2[list(labelling.values())[0]] = polynomial
    characteristic_weights.append(weight)


average_polynomial = np.average(matching_polynomials, 0, weights)
average_characteristic_polynomial = np.average(characteristic_polynomials, 0, characteristic_weights)
roots = np.roots(average_polynomial)
roots = np.round(roots, 3)
roots = sorted(roots)
print(average_polynomial)
print(roots)
characteristic_polynomials = list(np.unique(characteristic_polynomials, axis=0))
characteristic_polynomials_matrix = np.asarray(characteristic_polynomials)
characteristic_polynomials_matrix = characteristic_polynomials_matrix.transpose()
characteristic_polynomials.extend(list(np.unique(matching_polynomials, axis=0)))
characteristic_and_matching_polynomials_matrix = np.asarray(characteristic_polynomials)
characteristic_and_matching_polynomials_matrix = characteristic_and_matching_polynomials_matrix.transpose()
b = linalg.null_space(characteristic_and_matching_polynomials_matrix)
print(b)
# characteristic_polynomials.append(average_polynomial)
# characteristic_polynomials_with_average_matching_matrix = np.asarray(characteristic_polynomials)
# r1 = np.linalg.matrix_rank(characteristic_polynomials_matrix)
# r2 = np.linalg.matrix_rank(characteristic_polynomials_with_average_matching_matrix)
# print(r1, r2, characteristic_polynomials_matrix.shape)
# if r1 == r2:
#     x = np.linalg.lstsq(characteristic_polynomials_matrix, average_polynomial, rcond=None)
#     print(x[0])

print()