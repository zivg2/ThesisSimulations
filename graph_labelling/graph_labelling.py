from itertools import product
import networkx as nx
from networkx.algorithms.tree import maximum_spanning_tree
from elements_generator.elements_generator import ElementsGenerator

from typing import Tuple, TypeVar, List, Iterable, Dict, Generic
T = TypeVar("T")
S = TypeVar("S")


class GraphLabelling(Generic[T]):
    def __init__(self, elements_generator: ElementsGenerator[T]):
        self._elements_generator = elements_generator

    def labellings(self, graph: nx.Graph) -> Iterable[Dict[S, T]]:
        source = self._get_source(graph)

        elements = self._elements_generator.get_all_elements()

        for image in product(elements, repeat=len(source)):
            return_mapping = {x: image[source.index(x)]
                              for x in source}
            yield return_mapping

    def weighted_labellings(self, graph: nx.Graph) -> Iterable[Tuple[Dict[S, T], float]]:
        for labelling in self.labellings(graph):
            yield (labelling, 1)

    def random_labellings(self, graph: nx.Graph, amount: int) -> Iterable[Dict[S, T]]:
        for _ in range(amount):
            yield self.random_labelling(graph)

    def random_labelling(self, graph: nx.Graph) -> Dict[S, T]:
        source = self._get_source(graph)
        return_mapping = {source_element: self._elements_generator.random_element() for source_element in source}
        return return_mapping

    @staticmethod
    def _get_source(graph: nx.Graph) -> List[S]:
        source = graph.edges
        spanning_tree = maximum_spanning_tree(graph)
        source = [element for element in source if element not in spanning_tree.edges]
        return source


