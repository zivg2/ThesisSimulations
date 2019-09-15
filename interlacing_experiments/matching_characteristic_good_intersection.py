import networkx as nx
from networkx.convert_matrix import from_numpy_matrix
import numpy as np
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

q = 11
pgl2 = PGL2(q)
conjugation_classes = pgl2.get_conjugation_classes()
number_of_elements = sum(conjugation_classes.values())

triangular_subset = pgl2_upper_triangular(q)
number_of_triangular_elements = len(triangular_subset)

elements_generator = IterableElementsGenerator(triangular_subset)
projective_zero = pgl2.get_pf().zero()
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


s = q+1
# s = sympy.symbols("s")
m = []

elements = list(characteristic_polynomials.keys())
weights = []

for g in elements:
    if g in matching_polynomials:
        new_polynomial = list(characteristic_polynomials[g][1] * characteristic_polynomials[g][0]
                              - matching_polynomials[g][1]*matching_polynomials[g][0]*s)
        new_polynomial.append(matching_polynomials[g][1])
        m.append(np.asarray(new_polynomial))
    else:
        new_polynomial = list(characteristic_polynomials[g][1] * characteristic_polynomials[g][0])
        new_polynomial.append(0)
        m.append(np.asarray(new_polynomial))
    weights.append(characteristic_polynomials[g][1])


mat = np.asarray(m)
mat = mat.transpose()
original_result = np.asarray([0]* (q+1) + [1/s])

# printer = sympy.printing.str.StrPrinter()
# m1 = sympy.Matrix(mat)
# r1 = sympy.Matrix(original_result)
# aa = m1.col_insert(m1.shape[1], r1)
# bb = sympy.Matrix.zeros(aa.rows-1, aa.cols)
# bb = bb.row_insert(0, aa.row(aa.rows-1))
# aa = aa + bb*s
# aaa = sympy.linsolve((m1, r1))
result, ttt, rrr, sss = np.linalg.lstsq(mat, original_result, rcond=None)
result2, ttt2, rrr2, sss2 = np.linalg.lstsq(mat, [0]*(q+2), rcond=None)
print(np.abs(np.dot(mat, result) - original_result).max())
print(ttt, rrr, sum([result[i]*weights[i] for i in range(len(result))]))
elements_data = {elements[i]: (result[i], result[i]/weights[i]) for i in range(len(elements))}
for x in elements_data:
    print(x, elements_data[x])

print()