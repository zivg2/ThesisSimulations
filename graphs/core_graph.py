from .oriented_labelled_graph_with_basepoint import OrientedLabelledGraphWithBasePoint
from sympy.combinatorics.free_groups import FreeGroupElement


class CoreGraph(OrientedLabelledGraphWithBasePoint):
    def __init__(self):
        super().__init__()

    @classmethod
    def from_oriented_labelled_graph_with_base_point(cls, graph: OrientedLabelledGraphWithBasePoint):
        result = cls()
        result._graph = graph._graph
        return result

    def label_to_edge(self, node):
        edges = self.edges(node)
        return {edge[3]: (edge[1], edge[2]) for edge in edges}

    def is_member(self, x: FreeGroupElement):
        current_node = self.base_point()
        for letter in x.letter_form_elm:
            possible_nodes = self.label_to_edge(current_node)
            if letter not in possible_nodes:
                return False
            current_node = possible_nodes[letter][0]
        return current_node == self.base_point()

    def get_membership_path(self, x: FreeGroupElement):
        membership_path = []
        current_node = self.base_point()
        for letter in x.letter_form_elm:
            possible_nodes = self.label_to_edge(current_node)
            if letter not in possible_nodes:
                return membership_path
            membership_path.append((current_node, possible_nodes[letter][0], possible_nodes[letter][1], letter))
            current_node = possible_nodes[letter][0]
        return membership_path

    def fold_edge_pair(self, edge1, edge2):
        new_graph = self.identify_nodes(edge1[0], edge2[0])
        return CoreGraph.from_oriented_labelled_graph_with_base_point(new_graph.fold())

    def rank(self):
        return self._graph.number_of_edges() - self._graph.number_of_nodes() + 1

