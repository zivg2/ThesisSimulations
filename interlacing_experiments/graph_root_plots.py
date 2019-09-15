from representations import TransitiveActionUnitaryStandardRepresentation
from group_actions import PGLGroupAction
from projective_sets.pgl2 import PGL2
from graph_labelling import GraphLabelling
from graph_covering.graph_covering import GraphCovering
import networkx as nx
from utilities.general_utilities import *
from utilities.primes import odd_primes_up_to
from graph_covering.graph_covering_spectrum_analyzer import GraphCoveringSpectrumAnalyzer

qs = odd_primes_up_to(100)
next(qs); next(qs); next(qs); next(qs);next(qs)


n = 5
d = 4

graph = nx.random_regular_graph(d, n)
rho = get_rho(d)

for q in qs:
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    representation = TransitiveActionUnitaryStandardRepresentation(action, pgl2.get_pf().infinity())

    covering = GraphCovering(graph, representation)

    graph_labelling = GraphLabelling(pgl2)
    labellings = list(graph_labelling.random_labellings(graph, 100))

    adjacencies = [covering.adjacency(labelling) for labelling in labellings]

    roots = [sorted(GraphCoveringSpectrumAnalyzer.get_eigenvalues(matrix)) for matrix in adjacencies]
    roots = np.round(roots, 2)
    good_roots = []
    bad_roots = []
    good_roots_found = False
    for x in roots:
        if x.min() >= -rho and x.max() <= rho:
            good_roots.extend(x)
            good_roots_found = True
        else:
            bad_roots.extend(x)
    if good_roots_found:
        print('Found good roots for q=%d' % q)

    plot_complex_lists([bad_roots, good_roots])
