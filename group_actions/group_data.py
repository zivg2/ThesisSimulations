from graph_labelling import UpToConjugationGraphLabelling, GraphLabelling, DeterminantDataUpToConjugationGraphLabelling
from group_actions import *
from projective_sets.pgl2 import PGL2, PGL2Element
from utilities.general_utilities import measure, memorize
from representations import TransitiveActionUnitaryStandardRepresentation, \
    StandardRepresentation, SignRepresentation, TensorRepresentation
from elements_generator import ConditionalElementsGenerator, IterableElementsGenerator, ElementsGenerator
from graph_covering.graph_covering_spectrum import GraphCoveringSpectrum
from typing import Callable


def get_representation_class(is_unitary):
    if is_unitary:
        return TransitiveActionUnitaryStandardRepresentation
    else:
        return StandardRepresentation


@measure
@memorize
def get_pgl2_filtered_data(q, is_unitary, pgl_filter: Callable[[PGL2Element], bool]):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = ConditionalElementsGenerator(pgl2, pgl_filter)
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


@measure
@memorize
def get_pgl2_up_to_conjugation_filtered_data(q, is_unitary, pgl_filter: Callable[[PGL2Element], bool]):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = ConditionalElementsGenerator(pgl2, pgl_filter)
    conjugation_classes = pgl2.get_conjugation_classes()
    conjugation_classes = {element: conjugation_classes[element] for element in conjugation_classes
                           if pgl_filter(element)}
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


@measure
def get_pgl2_up_to_conjugation_with_determinant_data(q, is_unitary, determinant_data):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = pgl2
    conjugation_classes = pgl2.get_conjugation_classes()
    conjugation_classes = {element: conjugation_classes[element] for element in conjugation_classes}
    labelling = DeterminantDataUpToConjugationGraphLabelling(conjugation_classes, elements_generator, determinant_data)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


def get_pgl2_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = pgl2
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


def get_pgl2_up_to_conjugation_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = pgl2
    conjugation_classes = pgl2.get_conjugation_classes()
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


def get_pgl2_up_to_conjugation_signed_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    elements_generator = pgl2
    conjugation_classes = pgl2.get_conjugation_classes()
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = TensorRepresentation(representation_class(action, pgl2.get_pf().infinity()), SignRepresentation())
    return representation, labelling


def get_pgl2_partial_elements_data(q, is_unitary, elements):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    if isinstance(elements, ElementsGenerator):
        elements_generator = elements
    else:
        elements_generator = IterableElementsGenerator(elements)
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


def get_po2_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    pgl2 = PGL2(q)
    action = PGLGroupAction(pgl2)
    field = pgl2.get_field()
    elements = [pgl2.create2(field.one(), b, -b, field.one()) for b in field.get_all_elements()]
    elements.extend([pgl2.create2(field.zero(), field.one(), b, field.zero()) for b in [field.one(), -field.one()]])
    elements.extend([pgl2.create2(field.one(), b, b, -field.one()) for b in field.get_all_elements()])
    elements_generator = IterableElementsGenerator(elements)
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, pgl2.get_pf().infinity())
    return representation, labelling


def get_determinant_data_pgl(q, is_unitary, graph, rho):
    s2_data = get_sn_data(1, True)
    s2_covering_spectrum = GraphCoveringSpectrum(s2_data[0], s2_data[1], rho)
    s2_covering_spectrum.is_graph_ramanujan_liftable_deterministic(graph)
    s2_lift = s2_covering_spectrum.last_round_labelling
    determinant_data = {x: -1 if s2_lift[x][0] == 0 else 1 for x in s2_lift}
    return get_pgl2_up_to_conjugation_with_determinant_data(q, is_unitary, determinant_data)


def get_psl2_data(q, is_unitary):
    return get_pgl2_filtered_data(q, is_unitary, lambda element: element.det().legendre() == 1)


def get_psl2_up_to_conjugation_data(q, is_unitary):
    return get_pgl2_up_to_conjugation_filtered_data(q, is_unitary, lambda element: element.det().legendre() == 1)


def get_sn_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    action = SNGroupAction(q+1)
    elements_generator = action.get_elements_generator()
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, q)
    return representation, labelling


@memorize
def get_sn_up_to_conjugation_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    action = SNGroupAction(q+1)
    elements_generator = action.get_elements_generator()
    conjugation_classes = get_sn_conjugation_classes(q+1)
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = representation_class(action, q)
    return representation, labelling


@memorize
def get_cn_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    action = CNGroupAction(q+1)
    elements_generator = action.get_elements_generator()
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, q)
    return representation, labelling


@memorize
def get_d2n_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    action = D2NGroupAction(q+1)
    elements_generator = action.get_elements_generator()
    labelling = GraphLabelling(elements_generator)
    representation = representation_class(action, q)
    return representation, labelling


@memorize
def get_cn_up_to_conjugation_data(q, is_unitary):
    representation_class = get_representation_class(is_unitary)
    action = CNGroupAction(q+1)
    elements_generator = action.get_elements_generator()
    conjugation_classes = {0: 1}
    for i in range(1, q+1):
        d = math.gcd(i, q+1)
        if d not in conjugation_classes:
            conjugation_classes[d] = 0
        conjugation_classes[d] += 1
    labelling = UpToConjugationGraphLabelling(conjugation_classes, elements_generator)
    representation = representation_class(action, q)
    return representation, labelling
