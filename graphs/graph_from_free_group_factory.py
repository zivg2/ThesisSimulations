from .oriented_labelled_graph_with_basepoint import OrientedLabelledGraphWithBasePoint
from .core_graph import CoreGraph
from sympy.combinatorics.free_groups import FreeGroupElement
from typing import Iterable, List


class GraphFromFreeGroupFactory:
    @staticmethod
    def cycle_from_element(x: FreeGroupElement) -> OrientedLabelledGraphWithBasePoint:
        graph = OrientedLabelledGraphWithBasePoint()
        number_of_nodes = 1
        for letter in x.letter_form_elm:
            next_node = number_of_nodes if number_of_nodes < len(x) else 0
            previous_node = number_of_nodes - 1
            graph.add_node(next_node)
            graph.add_edge(previous_node, next_node, letter)
            number_of_nodes += 1
        return graph

    @staticmethod
    def graph_wedge_sum(graphs: List[OrientedLabelledGraphWithBasePoint]) -> OrientedLabelledGraphWithBasePoint:
        new_graph = OrientedLabelledGraphWithBasePoint()
        number_of_nodes = len(new_graph)
        for graph in graphs:
            node_mapping = {graph.base_point(): 0}
            for node in graph.nodes():
                if node not in node_mapping:
                    new_graph.add_node(node + number_of_nodes)
                    node_mapping[node] = node + number_of_nodes
            for edge in graph.positive_edges():
                new_graph.add_edge(node_mapping[edge[0]], node_mapping[edge[1]], edge[3])
            number_of_nodes += len(graph) - 1
        return new_graph

    @staticmethod
    def bouquet_from_elements(elements: Iterable[FreeGroupElement]) -> OrientedLabelledGraphWithBasePoint:
        graphs = [GraphFromFreeGroupFactory.cycle_from_element(x) for x in elements]
        return GraphFromFreeGroupFactory.graph_wedge_sum(graphs)

    @staticmethod
    def get_subgroup_core(generators: Iterable[FreeGroupElement]) -> CoreGraph:
        graph = GraphFromFreeGroupFactory.bouquet_from_elements(generators)
        return CoreGraph.from_oriented_labelled_graph_with_base_point(graph.fold())
