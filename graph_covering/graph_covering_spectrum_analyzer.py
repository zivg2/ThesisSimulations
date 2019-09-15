import scipy.linalg
from utilities.general_utilities import round_up_to, measure


class GraphCoveringSpectrumAnalyzer:
    def __init__(self, graph_covering, rho, pool = None):
        self.covering = graph_covering
        self.pool = pool
        self.rho = rho

    def pool_is_graph_ramanujan_liftable_with_labelling(self, labelling):
        result = self.is_graph_ramanujan_liftable_with_labelling(labelling)
        if result:
            print("AAA")

    def is_graph_ramanujan_liftable_with_labelling(self, labelling):
        lower_matrix = self.covering.lower_adjacency(labelling)
        result = self._are_upper_matrix_eigenvalues_less_than_rho(lower_matrix)
        return result

    def _are_upper_matrix_eigenvalues_less_than_rho(self, lower_matrix):
        new_eigenvalues = self.get_eigenvalues(lower_matrix)
        max_eigenvalue = round_up_to(new_eigenvalues.max())
        minus_min_eigenvalue = round_up_to(-new_eigenvalues.min())
        if max_eigenvalue <= self.rho and minus_min_eigenvalue <= self.rho:
            return True
        else:
            return False

    @staticmethod
    @measure
    def get_eigenvalues(lower_matrix):
        val = scipy.linalg.eigh(lower_matrix,
                                overwrite_a=True,
                                overwrite_b=True,
                                check_finite=False,
                                eigvals_only=True)
        return val

    def _are_matrix_eigenvalues_less_than_rho(self, matrix):
        new_eigenvalues = self._get_max_eigenvalue_full(matrix)
        max_eigenvalue = round_up_to(new_eigenvalues.max())
        minus_min_eigenvalue = round_up_to(-new_eigenvalues.min())
        if max_eigenvalue < self.rho and minus_min_eigenvalue < self.rho:
            return True
        else:
            return False

    @staticmethod
    @measure
    def _get_max_eigenvalue_full(matrix):
        val = scipy.linalg.eig(matrix,
                               overwrite_a=True,
                               overwrite_b=True,
                               check_finite=False,
                               )[0]
        return val
