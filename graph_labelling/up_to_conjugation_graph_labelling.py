from .graph_labelling import GraphLabelling, nx
from elements_generator import ElementsGenerator
from itertools import combinations_with_replacement, product

from typing import Dict, TypeVar, Iterable, Tuple
T = TypeVar("T")
S = TypeVar("S")


class UpToConjugationGraphLabelling(GraphLabelling[T]):
    def __init__(self, conjugation_classes: Dict[T, int], elements_generator: ElementsGenerator[T]):
        super().__init__(elements_generator)
        self._conjugation_classes = conjugation_classes

    def labellings(self, graph: nx.Graph) -> Iterable[Dict[S, T]]:
        source = self._get_source(graph)
        if len(source) == 0:
            return {}
        first_element = source[0]
        source_remainder = source[1:]

        elements = self._elements_generator.get_all_elements()

        for image in product(self._conjugation_classes.keys(), combinations_with_replacement(elements, len(source) - 1)):
            return_mapping = {x: image[1][source.index(x)-1]
                              for x in source_remainder}
            return_mapping[first_element] = image[0]
            yield return_mapping

    def weighted_labellings(self, graph: nx.Graph) -> Iterable[Tuple[Dict[S, T], float]]:
        source = self._get_source(graph)
        if len(source) == 0:
            return {}
        first_element = source[0]
        source_remainder = source[1:]

        elements = self._elements_generator.get_all_elements() if len(source) > 1 else []

        for image in product(self._conjugation_classes.keys(), combinations_with_replacement(elements, len(source) - 1)):
            return_mapping = {x: image[1][source.index(x)-1]
                              for x in source_remainder}
            return_mapping[first_element] = image[0]
            yield return_mapping, self._conjugation_classes[image[0]]
