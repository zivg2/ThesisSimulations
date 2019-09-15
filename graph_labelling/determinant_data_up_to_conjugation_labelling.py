from . import UpToConjugationGraphLabelling
from projective_sets.pgl2 import PGL2
import networkx as nx
from elements_generator import ConditionalElementsGenerator
from itertools import permutations, product
from utilities.general_utilities import class_property_memorize
from fields import SquareExtensionField

from typing import Dict, TypeVar, Iterable, Tuple
T = TypeVar("T")
S = TypeVar("S")


class DeterminantDataUpToConjugationGraphLabelling(UpToConjugationGraphLabelling):
    def __init__(self, conjugation_classes: Dict[T, int], pgl2: PGL2, determinant_data):
        elements_generator = ConditionalElementsGenerator(pgl2, lambda x: x.det().legendre() == 1)
        conjugation_classes = {x: conjugation_classes[x] for x in conjugation_classes if x.det().legendre() == 1}
        super().__init__(conjugation_classes, elements_generator)
        self._determinant_data = determinant_data
        self._pgl2 = pgl2

    @class_property_memorize
    def _get_determinant_inverse_matrix(self):
        field = self._pgl2.get_field()
        non_square = SquareExtensionField.get_non_square_element(field)
        return self._pgl2.create2(non_square, field.zero(), field.zero(), field.one())

    def _get_correct_determinant_matrix(self, matrix, edge):
        if edge not in self._determinant_data or self._determinant_data[edge] == 1:
            return matrix
        else:
            return matrix * self._get_determinant_inverse_matrix()

    def labellings(self, graph: nx.Graph) -> Iterable[Dict[S, T]]:
        source = self._get_source(graph)
        if len(source) == 0:
            return {}
        first_element = source[0]
        source_remainder = source[1:]

        elements = self._elements_generator.get_all_elements()

        for image in product(self._conjugation_classes.keys(), permutations(elements, len(source) - 1)):
            return_mapping = {x: self._get_correct_determinant_matrix(
                                    image[1][source.index(x)-1], x
                                 )
                              for x in source_remainder}
            return_mapping[first_element] = self._get_correct_determinant_matrix(image[0], first_element)
            yield return_mapping

    def weighted_labellings(self, graph: nx.Graph) -> Iterable[Tuple[Dict[S, T], float]]:
        source = self._get_source(graph)
        if len(source) == 0:
            return {}
        first_element = source[0]
        source_remainder = source[1:]

        elements = self._elements_generator.get_all_elements()

        for image in product(self._conjugation_classes.keys(), permutations(elements, len(source) - 1)):
            return_mapping = {x: self._get_correct_determinant_matrix(
                                    image[1][source.index(x)-1], x
                                 )
                              for x in source_remainder}
            return_mapping[first_element] = self._get_correct_determinant_matrix(
                                                image[0], first_element
                                            )
            yield return_mapping, self._conjugation_classes[image[0]]

    def random_labelling(self, graph: nx.Graph) -> Dict[S, T]:
        source = self._get_source(graph)
        return_mapping = {source_element:
                          self._get_correct_determinant_matrix(
                              self._elements_generator.random_element(), source_element
                          ) for source_element in source}
        return return_mapping

