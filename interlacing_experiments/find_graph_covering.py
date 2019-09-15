import multiprocessing

from group_actions.group_data import *
from graph_covering.graph_covering_spectrum import GraphCoveringSpectrum
from utilities.primes import *
from utilities.my_polynomial import MyPolynomial
from utilities.general_utilities import *
import random
from graphs.graphs import *

number_of_graphs = 100000

is_unitary = True


def analyze_graph_polynomial(graph, graph_covering_spectrum: GraphCoveringSpectrum, rho):
    p = graph_covering_spectrum.return_average_lifts_characteristic_polynomial(graph)
    roots = np.roots(p)
    pp = MyPolynomial(np.flip(p, 0))
    print(pp)
    print(max(roots), rho)
    return p


def get_n_d():
    n = random.randint(4, 8)
    if not n % 2:
        d = random.randint(2, n-1)
    else:
        d = random.randint(1, n//2) * 2

    return n, d


def get_n_d_unbounded():
    n = random.randint(4, 10)
    if not n % 2:
        d = random.randint(3, 8)
    else:
        d = random.randint(2, 4//2) * 2

    return n, d


def get_connected_graph_by_generator(graph_generator):
    graph = graph_generator()
    if nx.is_connected(graph):
        return graph
    else:
        return get_connected_graph_by_generator(graph_generator)


@measure
def main():
    single_process = True
    if single_process:
        for graph_number in range(number_of_graphs):
            main_iteration(graph_number)
    else:
        pool = multiprocessing.Pool(4)
        pool.map(main_iteration, range(number_of_graphs))


repeats = 4
qs = list(odd_primes_up_to(2000))
max_tries = 0

file = open(r'results/covering_tests.txt', 'a')

@measure
def main_iteration(iteration):
    global max_tries
    q = qs.pop(0)
    graph = special_3_regular()
    d = 3
    n = 16
    rho = get_rho(d)
    user_data = 'q=%d, n=%d, d=%d' % (q, n, d)
    print(user_data)

    action_data = get_pgl2_up_to_conjugation_data(q, True)

    graph_covering_spectrum = GraphCoveringSpectrum(action_data[0], action_data[1], rho)
    liftable = graph_covering_spectrum.is_graph_ramanujan_liftable(graph)
    if not liftable:
        liftable = graph_covering_spectrum.is_graph_ramanujan_liftable_deterministic(graph)
    tries = graph_covering_spectrum.last_round_tries
    if max_tries < graph_covering_spectrum.max_tries:
        max_tries = graph_covering_spectrum.max_tries
        print('^%d' % max_tries)
    if not liftable:
        print(graph.out_edges())
        print(iteration)
    else:
        print(graph_covering_spectrum.last_round_labelling)
        file.write("%s, tries= %d\n" % (user_data, tries))
        file.flush()


def main_iteration_for_measurements(iteration):
    global max_tries
    if iteration // repeats >= len(qs):
        return
    q = qs[(iteration // repeats) % len(qs)]
    if not iteration % repeats:
        print('q = %d' % q)
    pgl2_data = get_pgl2_data(q, True)
    graph = nx.random_regular_graph(d, n)
    graph_covering_spectrum = GraphCoveringSpectrum(pgl2_data[0], pgl2_data[1], rho)
    liftable = graph_covering_spectrum.is_graph_ramanujan_liftable(graph)
    max_tries = max(max_tries, graph_covering_spectrum.max_tries)
    if not liftable:
        print(iteration)


if __name__ == "__main__":
    main()
    measure_mapping = get_measure_mapping()
    print(max_tries)
    file.close()
    print("Done!")
