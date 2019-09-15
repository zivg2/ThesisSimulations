import networkx as nx
import numpy as np
from utilities.my_polynomial import MyPolynomial
from scipy.optimize import minimize
from graph_labelling import UpToConjugationGraphLabelling
from graph_covering.graph_covering import GraphCovering
from representations import TransitiveActionUnitaryStandardRepresentation
from projective_sets.pxl2_subsets import *
from group_actions.pgl2_group_action import PGLGroupAction


def get_minimizing_function(mat, expected_result):
    def minimizing_function(x):
        diff = np.dot(mat, x) - expected_result
        return np.linalg.norm(diff)
    return minimizing_function


graph = nx.configuration_model((2,))

q = 5
pgl2 = PGL2(q)
conjugation_classes = pgl2.get_conjugation_classes()
number_of_elements = sum(conjugation_classes.values())

action2 = PGLGroupAction(pgl2)
representation = TransitiveActionUnitaryStandardRepresentation(action2, pgl2.get_pf().infinity())
graph_labelling = UpToConjugationGraphLabelling(conjugation_classes, pgl2)
graph_covering = GraphCovering(graph, representation)

characteristic_polynomials = {}

for labelling, weight in graph_labelling.weighted_labellings(graph):
    polynomial = graph_covering.get_polynomial(labelling)
    characteristic_polynomials[list(labelling.values())[0]] = (polynomial, weight)


m = []

elements = list(characteristic_polynomials.keys())

for g in characteristic_polynomials:
    m.append(characteristic_polynomials[g][1] * characteristic_polynomials[g][0])

mat = np.asarray(m)
mat = mat.transpose()
cols = len(characteristic_polynomials)
original_result = np.asarray([1] + [0] * (mat.shape[0]-1))

guess = np.asarray([1/number_of_elements] * len(characteristic_polynomials))
sol = minimize(get_minimizing_function(mat, original_result), guess, method='L-BFGS-B', bounds=[(0, None) for x in range(cols)])
x = sol['x']
print(x[:len(characteristic_polynomials)])
print(x[len(characteristic_polynomials):])
poly = np.round(np.dot(mat[:, :len(characteristic_polynomials)], x[:len(characteristic_polynomials)]), 2)
print(poly)
print(MyPolynomial(np.flip(poly, 0)))
print(np.dot(mat[:, :len(characteristic_polynomials)], x[:len(characteristic_polynomials)]))
print(sol['fun'])

print()