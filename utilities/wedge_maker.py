import numpy as np
from itertools import combinations, permutations
from group_actions.group_utiliies import permutation_parity


class WedgeMaker:
    def __init__(self, power):
        self.power = power

        get_wedge_matrix_mapping = {
            2: self._get_wedge_matrix_dim_2,
            3: self._get_wedge_matrix_dim_3
        }
        if self.power in get_wedge_matrix_mapping:
            get_wedge_matrix = get_wedge_matrix_mapping[self.power]
        else:
            get_wedge_matrix = self._get_wedge_matrix_dim_k
        self._get_wedge_matrix = get_wedge_matrix

    def get_wedge_matrix(self, matrix):
        return self._get_wedge_matrix(matrix)

    def _get_wedge_matrix_dim_2(self, matrix):
        basis_indices = self.get_wedge_basis_indices(matrix.shape[0])
        result = []
        for indices in basis_indices:
            vectors = [matrix[i, :] for i in indices]
            wedge_vector = self._get_wedge2(vectors, basis_indices)
            result.append(wedge_vector)
        return np.transpose(np.asarray(result))

    @staticmethod
    def _get_wedge2(vectors, basis_indices) -> np.ndarray:
        result = []
        for indices in basis_indices:
            temp_additive = vectors[0][indices[0]] * vectors[1][indices[1]] \
                            - vectors[0][indices[1]] * vectors[1][indices[0]]
            result.append(temp_additive)
        return np.asarray(result)

    def _get_wedge_matrix_dim_3(self, matrix):
        basis_indices = self.get_wedge_basis_indices(matrix.shape[0])
        result = []
        for indices in basis_indices:
            vectors = [matrix[i, :] for i in indices]
            wedge_vector = self._get_wedge3(vectors, basis_indices)
            result.append(wedge_vector)
        return np.transpose(np.asarray(result))

    @staticmethod
    def _get_wedge3(vectors, basis_indices) -> np.ndarray:
        result = []
        for indices in basis_indices:
            temp_additive = + vectors[0][indices[0]] * vectors[1][indices[1]] * vectors[2][indices[2]] \
                            + vectors[0][indices[1]] * vectors[1][indices[2]] * vectors[2][indices[0]] \
                            + vectors[0][indices[2]] * vectors[1][indices[0]] * vectors[2][indices[1]] \
                            - vectors[0][indices[0]] * vectors[1][indices[2]] * vectors[2][indices[1]] \
                            - vectors[0][indices[2]] * vectors[1][indices[1]] * vectors[2][indices[0]] \
                            - vectors[0][indices[1]] * vectors[1][indices[0]] * vectors[2][indices[2]]
            result.append(temp_additive)
        return np.asarray(result)

    def _get_wedge_matrix_dim_k(self, matrix):
        basis_indices = self.get_wedge_basis_indices(matrix.shape[0])
        result = [[np.linalg.det(matrix[self._get_minor_indices(indices2, indices)])
                  for indices2 in basis_indices] for indices in basis_indices]
        return np.asarray(result)

    def get_wedge_basis_indices(self, dimension):
        return list(combinations(range(dimension), self.power))

    @staticmethod
    def _get_minor_indices(indices, indices2):
        return np.ix_(indices, indices2)

    def _call_from_base_call(self, matrix):
        basis_indices = self.get_wedge_basis_indices(matrix.shape[0])
        result = []
        for indices in basis_indices:
            vectors = [matrix[i, :] for i in indices]
            wedge_vector = self._get_wedge(vectors, basis_indices)
            result.append(wedge_vector)
        return np.transpose(np.asarray(result))

    @staticmethod
    def _get_wedge(vectors, basis_indices) -> np.ndarray:
        result = []
        for indices in basis_indices:
            temp_additive = 0
            indices_enumeration = range(len(indices))
            for indices_permutation in permutations(indices_enumeration):
                temp = permutation_parity(indices_permutation)
                temp = temp
                for i in range(len(vectors)):
                    temp *= vectors[i][indices[indices_permutation[i]]]
                temp_additive += temp
            result.append(temp_additive)
        return np.asarray(result)
