from itertools import product
from operator import mul
from functools import reduce
import networkx as nx
from typing import Tuple, Iterable, Dict
from .graph_labelling import GraphLabelling, S, T
from elements_generator import IterableElementsGenerator


class WeightedGraphLabelling(GraphLabelling[T]):
    def __init__(self, weighted_elements: Dict[T, float]):
        self._weighted_elements = weighted_elements
        elements_generator = IterableElementsGenerator(self._weighted_elements.keys())
        super().__init__(elements_generator)

    def weighted_labellings(self, graph: nx.Graph) -> Iterable[Tuple[Dict[S, T], float]]:
        source = self._get_source(graph)

        for image in product(self._weighted_elements, repeat=len(source)):
            return_mapping = {x: image[source.index(x)]
                              for x in source}
            weight = reduce(mul, [self._weighted_elements[image[i]] for i in range(len(source))])
            yield return_mapping, weight



