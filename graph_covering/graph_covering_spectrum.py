import numpy as np
import multiprocessing

from .graph_covering import GraphCovering
from .graph_covering_spectrum_analyzer import GraphCoveringSpectrumAnalyzer
from representations import Representation
from utilities.general_utilities import measure
from graph_labelling import GraphLabelling


class GraphCoveringSpectrum:
    def __init__(self, representation: Representation, graph_labelling: GraphLabelling, rho: float):
        self.max_tries = 0
        self.representation = representation
        self.graph_labelling = graph_labelling
        self.number_of_tries = 1000
        self.rho = rho
        self.random_functions = True
        self.multi_processes = 1
        if self.multi_processes > 1:
            self.pool = multiprocessing.Pool(self.multi_processes)
        else:
            self.pool = None
        self.last_round_tries = 0
        self.last_round_labelling = None

    @measure
    def is_graph_ramanujan_liftable(self, graph):
        labellings = self._get_labellings(graph)
        liftable = self._is_graph_ramanujan_liftable_with_possible_labellings(graph, labellings)
        return liftable

    @measure
    def is_graph_ramanujan_liftable_randomly(self, graph):
        random_functions_previous = self.random_functions
        self.random_functions = True
        result = self.is_graph_ramanujan_liftable(graph)
        self.random_functions = random_functions_previous
        return result

    @measure
    def is_graph_ramanujan_liftable_deterministic(self, graph):
        random_functions_previous = self.random_functions
        self.random_functions = False
        result = self.is_graph_ramanujan_liftable(graph)
        self.random_functions = random_functions_previous
        return result

    def _get_labellings(self, graph):
        if self.random_functions:
            labellings = self.graph_labelling.random_labellings(graph, self.number_of_tries)
        else:
            labellings = self.graph_labelling.labellings(graph)
        return labellings

    def _is_graph_ramanujan_liftable_with_possible_labellings(self, graph, possible_labellings):
        graph_covering = GraphCovering(graph, self.representation)
        covering_analyzer = GraphCoveringSpectrumAnalyzer(graph_covering, self.rho, self.pool)

        if self.multi_processes > 1:
            self.pool.map(covering_analyzer.pool_is_graph_ramanujan_liftable_with_labelling, possible_labellings)
            return True
        else:
            return self._is_graph_ramanujan_liftable_with_possible_labellings_single_process(covering_analyzer,
                                                                                             possible_labellings)

    def _is_graph_ramanujan_liftable_with_possible_labellings_single_process(self, covering_analyzer,
                                                                             possible_labellings):
        count = 0
        for labelling in possible_labellings:
            count += 1
            result = covering_analyzer.is_graph_ramanujan_liftable_with_labelling(labelling)

            if result:
                self.last_round_tries = count
                self.last_round_labelling = labelling
                self.max_tries = max(self.max_tries, count)
                return True
        return False

    @measure
    def return_average_lifts_characteristic_polynomial(self, graph):
        weighted_labellings = self.graph_labelling.weighted_labellings(graph)
        graph_covering = GraphCovering(graph, self.representation)
        polynomials = []
        weights = []
        for labelling, weight in weighted_labellings:
            polynomial = graph_covering.get_polynomial(labelling)
            polynomials.append(polynomial)
            weights.append(weight)
        average_polynomial = np.average(polynomials, 0, weights)
        return average_polynomial

    @measure
    def return_average_lifts_activated_characteristic_polynomial(self, graph, activation):
        weighted_labellings = self.graph_labelling.weighted_labellings(graph)
        graph_covering = GraphCovering(graph, self.representation)
        polynomials = []
        weights = []
        for labelling, weight in weighted_labellings:
            adjacency = graph_covering.adjacency(labelling)
            m = activation(adjacency)
            polynomial = graph_covering.get_matrix_polynomial(m)
            polynomials.append(polynomial)
            weights.append(weight)
        average_polynomial = np.average(polynomials, 0, weights)
        return average_polynomial

    @measure
    def return_average_random_lifts_characteristic_polynomial(self, graph):
        labellings = self.graph_labelling.random_labellings(graph, self.number_of_tries)
        graph_covering = GraphCovering(graph, self.representation)
        polynomials = []
        for labelling in labellings:
            polynomial = graph_covering.get_polynomial(labelling)
            polynomials.append(polynomial)
        average_polynomial = np.average(polynomials, 0)
        return average_polynomial
