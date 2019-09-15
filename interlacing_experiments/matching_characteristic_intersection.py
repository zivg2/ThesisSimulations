import networkx as nx
from networkx.convert_matrix import from_numpy_matrix
import numpy as np
from utilities.my_polynomial import MyPolynomial
from scipy.optimize import minimize
from graph_labelling import UpToConjugationGraphLabelling
from graph_covering.graph_covering import GraphCovering
from graphs.graph_utilities import get_matching_polynomial
from representations import PermutationRepresentation, TransitiveActionUnitaryStandardRepresentation
from projective_sets.pxl2_subsets import *
from group_actions.pgl2_group_action import PGLGroupAction
from group_actions.sn_group_action import SNGroupAction
from group_actions.group_utiliies import *


def get_minimizing_function(mat, expected_result):
    def minimizing_function(x):
        diff = np.dot(mat, x) - expected_result
        return np.linalg.norm(diff)
    return minimizing_function


graph = nx.configuration_model((2,))

q = 7
pgl2 = PGL2(q)
conjugation_classes = pgl2.get_conjugation_classes()
number_of_elements = sum(conjugation_classes.values())

action = SNGroupAction(q)
elements_generator = action.get_elements_generator()
up_to_conjugation_elements = get_sn_conjugation_classes(q)

number_of_triangular_elements = sum(up_to_conjugation_elements.values())
graph_labelling = UpToConjugationGraphLabelling(up_to_conjugation_elements, elements_generator)
representation = PermutationRepresentation(action)
graph_covering = GraphCovering(graph, representation)

action2 = PGLGroupAction(pgl2)
representation2 = TransitiveActionUnitaryStandardRepresentation(action2, pgl2.get_pf().infinity())
graph_labelling2 = UpToConjugationGraphLabelling(conjugation_classes, pgl2)
graph_covering2 = GraphCovering(graph, representation2)

matching_polynomials = {}
characteristic_polynomials = {}

for labelling, weight in graph_labelling.weighted_labellings(graph):
    adjacency = graph_covering.adjacency(labelling).astype(int)
    lifted_graph = from_numpy_matrix(adjacency, create_using=nx.MultiGraph, parallel_edges=True)
    polynomial = get_matching_polynomial(lifted_graph)
    matching_polynomials[list(labelling.values())[0]] = (polynomial, weight)

for labelling, weight in graph_labelling2.weighted_labellings(graph):
    polynomial = graph_covering2.get_polynomial(labelling)
    characteristic_polynomials[list(labelling.values())[0]] = (polynomial, weight)


m = []

elements = list(characteristic_polynomials.keys())

for g in characteristic_polynomials:
    m.append(characteristic_polynomials[g][1] * characteristic_polynomials[g][0])

for g in matching_polynomials:
    m.append(-matching_polynomials[g][1] * matching_polynomials[g][0])


mat = np.asarray(m)
mat = mat.transpose()
cols = len(characteristic_polynomials) + len(matching_polynomials)
array1 = np.asarray([characteristic_polynomials[g][1] for g in characteristic_polynomials.keys()]
                    + [0]*len(matching_polynomials)).reshape((1, cols))
array2 = np.asarray([0]*len(characteristic_polynomials) +
                    [matching_polynomials[g][1] for g in matching_polynomials]).reshape((1, cols))
mat = np.append(mat, array1,axis=0)
mat = np.append(mat, array2,axis=0)
original_result = np.asarray([0] * (mat.shape[0]-2) + [1] * 2)

guess = np.asarray([1/number_of_elements] * len(characteristic_polynomials) + [1/number_of_triangular_elements] * len(matching_polynomials))
# guess = np.asarray([1]*cols)
sol = minimize(get_minimizing_function(mat, original_result), guess, method='L-BFGS-B', bounds=[(0., None) for x in range(cols)])
x = sol['x']
print(x[:len(characteristic_polynomials)])
print(x[len(characteristic_polynomials):])
poly = np.round(np.dot(mat[:-2, :len(characteristic_polynomials)], x[:len(characteristic_polynomials)]), 2)
print(poly)
print(MyPolynomial(np.flip(poly, 0)))
print(np.dot(mat[-2:, :len(characteristic_polynomials)], x[:len(characteristic_polynomials)]))
print(sol['fun'])

print()