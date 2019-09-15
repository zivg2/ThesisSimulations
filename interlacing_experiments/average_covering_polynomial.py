from utilities.general_utilities import get_measure_mapping, round_up_to, subsets
from group_actions.group_data import *
from group_actions.pgl2_s_mod_pgl2_action import PGL2SModPGL2GroupAction
from graph_labelling import WeightedGraphLabelling
from graph_covering.graph_covering_spectrum import GraphCoveringSpectrum
from math import sqrt
import networkx as nx
import numpy as np
from utilities.my_polynomial import MyPolynomial
from scipy.misc import comb
from representations.characters import Character
from representations import PermutationRepresentation, TrivialRepresentation
from graph_covering.graph_covering import GraphCovering
from projective_sets.pxl2_subsets import *
from representations import TransitiveActionUnitaryStandardRepresentation, SumRepresentation
from representations.pgl2.pgl2_cuspidal_representation import PGL2CuspidalRepresentation
from representations.pgl2.pgl2_principal_representation import PGL2PrincipalRepresentation


def weighted_pgl2_data(q, is_unitary, character: Character):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements = pgl2.get_all_elements()
    weighted_elements = {element: abs(round_up_to(np.real(character.apply(element)))) for element in elements}
    labelling = WeightedGraphLabelling(weighted_elements)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


@measure
def create_human_readable_polynomial(action_data):
    graph_covering_spectrum = GraphCoveringSpectrum(action_data[0], action_data[1], rho)
    p = graph_covering_spectrum.return_average_lifts_characteristic_polynomial(graph)
    roots = sorted(np.roots(p))
    pp = MyPolynomial(np.flip(p, 0))
    print(count, pp)
    print(roots[0: 2], roots[-2:])
    mobius_p = mobius_transform_polynomial(p, rho)
    mobius_pp = MyPolynomial(np.flip(mobius_p, 0))
    print(mobius_p.min(), mobius_pp)


@measure
def create_random_human_readable_polynomial(action_data):
    graph_covering_spectrum = GraphCoveringSpectrum(action_data[0], action_data[1], rho)
    p = graph_covering_spectrum.return_average_random_lifts_characteristic_polynomial(graph)
    roots = sorted(np.roots(p))
    pp = MyPolynomial(np.flip(p, 0))
    print(count, pp)
    print(roots[0: 2], roots[-2:])
    mobius_p = mobius_transform_polynomial(p, rho)
    print(mobius_p.min(), MyPolynomial(np.flip(mobius_p, 0)))


@measure
def create_human_readable_polynomial_a_a_transpose(action_data):
    graph_covering_spectrum = GraphCoveringSpectrum(action_data[0], action_data[1], rho)
    activation = lambda x: np.matmul(x, np.transpose(x))
    p = graph_covering_spectrum.return_average_lifts_activated_characteristic_polynomial(graph, activation)
    roots = sorted(np.roots(p))
    print(roots[0: 2], roots[-2:])


@measure
def polynomials(representation, elements):
    temp = elements
    temp = [representation.apply(x) for x in temp]
    temp = [np.poly(x) for x in temp]
    temp = [np.flip(x, 0) for x in temp]
    temp = [np.round(x * 1000) / 1000 for x in temp]
    return [MyPolynomial(x) for x in temp]


@measure
def labelling_polynomials_roots(graph: nx.Graph,
                                graph_covering: GraphCovering,
                                graph_labellings: GraphLabelling):
    for labelling in graph_labellings.labellings(graph):
        roots2 = sorted(np.linalg.eigvals(graph_covering.adjacency(labelling)))
        polynomial = graph_covering.get_polynomial(labelling)
        roots = sorted(np.roots(polynomial))
        print(roots[0: 2], roots[-2:])
        print(roots2[0: 2], roots2[-2:])


def k_sum_coefficient(d, j, n):
    k_min = max(0, n+j-d)
    k_max = min(n, j)
    positive_sum = sum([comb(j, k)*comb(d-j, n-k) for k in range(k_min, k_max+1, 2)])
    negative_sum = sum([comb(j, k)*comb(d-j, n-k) for k in range(k_min+1, k_max+1, 2)])
    if k_min % 2 == 0:
        return positive_sum - negative_sum
    else:
        return negative_sum - positive_sum


def mobius_transform_polynomial(p, r):
    d = p.shape[0]-1
    p0 = np.poly1d(p)
    p_curr = p0
    derivatives = [p0]
    for k in range(1, d+1):
        p_curr = np.polyder(p_curr)
        derivatives.append(p_curr)
    coefficients = []
    derivative_values = [x(-r) for x in derivatives]
    k_coefficients = [((2 * r) ** k) / np.math.factorial(k) * derivative_values[k] for k in range(d + 1)]
    for n in range(d+1):
        coefficient = sum([k_coefficients[k]*scipy.misc.comb(d-k, n-k) for k in range(n+1)])
        if (n-d)% 2 != 0:
            coefficient = -coefficient
        coefficients.append(coefficient)
    return np.asarray(coefficients)


n = 1
d = 2
rho = 2*sqrt(d-1)

graph = nx.configuration_model((d,)*n)
print(graph.edges)
print(rho)

qs = odd_primes_up_to(100)

for q in qs:
    print('q = %d' % q)
    group = PGL2(q)
    psl = PSL2(q)
    field = group.get_field()
    count = 0

    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    action2 = PGL2SModPGL2GroupAction(q)
    elements_generator = pgl2
    conjugation_classes = pgl2.get_conjugation_classes()
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = StandardRepresentation(action, pgl2.get_pf().infinity())
    action_data_pairs = [(representation, labelling)]

    for action_data in action_data_pairs:
        graph_covering_spectrum = GraphCoveringSpectrum(action_data[0], action_data[1], rho)
        p = graph_covering_spectrum.return_average_lifts_characteristic_polynomial(graph)
        roots = [x for x in np.roots(p)]
        roots = sorted(roots)
        roots = np.round(roots, 2)
        print(roots)
        print()

    print()

measure_mapping = get_measure_mapping()
print("DONE!")
