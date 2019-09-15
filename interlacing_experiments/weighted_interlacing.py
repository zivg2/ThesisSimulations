import networkx as nx
import numpy as np
from graph_covering.graph_covering import GraphCovering
from graph_labelling.graph_labelling import GraphLabelling
from graph_labelling.up_to_conjugation_graph_labelling import UpToConjugationGraphLabelling
from representations import TransitiveActionUnitaryStandardRepresentation
from group_actions import PGLGroupAction
from projective_sets.pgl2 import PGL2
from utilities.my_polynomial import MyPolynomial
from copy import copy
from itertools import product, combinations, combinations_with_replacement
from operator import mul
from functools import reduce
from math import log
from representations.characters.wedge_character import WedgeCharacter

q = 5


graph = nx.configuration_model((2,))
graph2 = nx.configuration_model((4,))


pgl2 = PGL2(q)
action = PGLGroupAction(pgl2)
representation = TransitiveActionUnitaryStandardRepresentation(action, pgl2.get_pf().infinity())
characters = [WedgeCharacter.create_wedge_character(representation, i) for i in range(q+1)]
conjugation_classes = list(pgl2.get_conjugation_classes().keys())


graph_covering = GraphCovering(graph, representation)
graph_covering2 = GraphCovering(graph2, representation)
graph_labelling = UpToConjugationGraphLabelling(pgl2.get_conjugation_classes(), pgl2)


def trace_measure(x):
    return q - characters[1].apply(x)


def cycle_length_measure_1(x):
    fixed_points = characters[1].apply(x)
    fixed_points = round(fixed_points)+1
    if fixed_points == q+1:
        return 1/(q*(q+1))
    elif fixed_points == 2:
        return 0
    elif fixed_points == 1:
        return 1/(q*(q+1))
    elif fixed_points == 0:
        y = x
        a = 1
        while characters[1].apply(y) != q:
            y *= x
            a += 1
        return 2/(q**3-q) * (-1)**((q+1)//a-1)
    else:
        raise ArithmeticError()


def get_polynomials_and_weights(graph, graph_covering, graph_labelling, measure):
    polynomials = []
    weights = []
    for labelling, weight in graph_labelling.weighted_labellings(graph):
        coefficient = measure_labelling(labelling, measure)
        if coefficient == 0:
            continue
        polynomial = graph_covering.get_polynomial(labelling)
        polynomials.append(polynomial)
        weights.append(weight * coefficient)
    return polynomials, weights


def measure_labelling(labelling, measure):
    labelling_values = list(labelling.values())
    tr = [measure(labelling_value) for labelling_value in labelling_values]
    coefficient = reduce(mul, tr)
    return coefficient


def get_measure(elements, element_weights):
    def helper(x):
        y = pgl2.get_conjugation_class(x)
        i = elements.index(y)
        return element_weights[i]
    return helper


def get_measures(elements, k):
    for element_weight_sums in combinations_with_replacement(range(k+1), r=len(elements)-1):
        element_weights = [element_weight_sums[0]]
        element_weights += [element_weight_sums[i] - element_weight_sums[i-1] for i in range(1, len(elements)-1)]
        element_weights += [k - element_weight_sums[-1]]

        yield get_measure(elements, element_weights)


def print_good_measures_for_graph(good_measures, graph, graph_covering):
    for measure_list in good_measures:
        measure = get_measure(conjugation_classes, measure_list)
        if not is_measure_good(measure, graph, graph_covering):
            print(measure_list)


def is_measure_good(measure, graph, graph_covering):
    polynomials, weights = get_polynomials_and_weights(graph, graph_covering, graph_labelling, measure)
    average_polynomial = np.average(polynomials, 0, weights)
    roots = np.roots(average_polynomial)
    roots = np.round(roots, 3)
    return (np.imag(roots) == 0).all()


print(conjugation_classes)

good_measures = []
for measure in get_measures(conjugation_classes, 2*len(conjugation_classes)):
    polynomials, weights = get_polynomials_and_weights(graph, graph_covering, graph_labelling, measure)
    average_polynomial = np.average(polynomials, 0, weights)
    roots = np.roots(average_polynomial)
    roots = np.round(roots, 3)
    if (np.imag(roots) == 0).all():
        print([measure(x) for x in conjugation_classes], average_polynomial)
        good_measures.append([measure(x) for x in conjugation_classes])

print()
print("Done1")

s = 20

for measure_weights in good_measures:
    measure = get_measure(conjugation_classes, measure_weights)
    polynomials, weights = get_polynomials_and_weights(graph2, graph_covering2, graph_labelling, measure)
    average_polynomial = np.average(polynomials, 0, weights)
    roots = np.roots(average_polynomial)
    roots = np.round(roots, 3)
    if (np.imag(roots) == 0).all():
        print([measure(x) for x in conjugation_classes])
