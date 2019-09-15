import numpy as np
import networkx as nx
from representations import Representation, UnitaryRepresentation
from utilities.general_utilities import *


class GraphCovering:
    def __init__(self, graph: nx.Graph, representation: Representation):
        self.representation = representation
        self.edges = graph.edges
        self._dim = representation.dim()
        self._identity = np.eye(self._dim)
        self._size = graph.number_of_nodes() * self._dim

    @measure
    def lower_adjacency(self, labelling):
        result = np.zeros((self._size, self._size))
        for edge in self.edges:
            if edge in labelling:
                block = self.representation.apply(labelling[edge])
            else:
                block = self._identity
            self._extend_matrix(result, edge, block)

            if edge[0] == edge[1]:
                self._extend_matrix(result, edge, np.linalg.inv(block))
        return np.transpose(result)

    def get_polynomial(self, labelling):
        matrix = self.adjacency(labelling)
        polynomial = self.get_matrix_polynomial(matrix)
        return polynomial

    @staticmethod
    @measure
    def get_matrix_polynomial(matrix):
        polynomial = np.poly(matrix)
        polynomial = np.round(polynomial)
        return polynomial

    def adjacency(self, labelling):
        if isinstance(self.representation, UnitaryRepresentation):
            return self._unitary_adjacency(labelling)
        else:
            return self._normal_adjacency(labelling)

    @measure
    def _normal_adjacency(self, labelling):
        result = np.zeros((self._size, self._size), dtype=complex)
        for edge in self.edges:
            if edge in labelling:
                normal_block = self.representation.apply(labelling[edge])
                inverse_block = np.linalg.inv(normal_block)
            else:
                normal_block = self._identity
                inverse_block = self._identity
            self._extend_matrix(result, edge, normal_block)
            self._extend_matrix(result, self._inverse_edge(edge), inverse_block)
        return result

    @measure
    def _unitary_adjacency(self, labelling):
        result = np.zeros((self._size, self._size))
        for edge in self.edges:
            if edge in labelling:
                normal_block = self.representation.apply(labelling[edge])
            else:
                normal_block = self._identity
            self._extend_matrix(result, edge, normal_block)
        result += np.transpose(result)
        return result

    @measure
    def _extend_matrix(self, matrix, edge, labelling_representation):
        v0 = edge[0]
        v1 = edge[1]
        matrix[v0 * self._dim: (v0 + 1) * self._dim, v1 * self._dim: (v1 + 1) * self._dim] += labelling_representation

    @staticmethod
    def _inverse_edge(edge):
        if len(edge) == 3:
            return edge[1], edge[0], edge[2]
        else:
            return edge[1], edge[0]



