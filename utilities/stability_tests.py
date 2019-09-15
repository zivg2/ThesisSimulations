import numpy as np


class StabilityTests:
    @staticmethod
    def lienard_chipart(p):
        """
        :param p: p[0]*x**d + p[1]*x**(d-1)+...
        :return: True iff the polynomial's roots have only negative real parts
        """
        d = len(p) - 1
        if p[0] < 0:
            p = -p
        if d == 0:
            return True
        if d == 1:
            return p[1] > 0
        hurwitz_matrix = [[0] * (i // 2) +
                          [p[j] for j in range(1 - (i % 2), d+1, 2)] +
                          [0] * ((d - i) // 2) for i in range(d+1)]
        hurwitz_matrix = np.asarray(hurwitz_matrix)
        determinants = [p[d], p[d-2]]
        determinants += [np.linalg.det(hurwitz_matrix[:i, :i]) for i in range(1, d+1, 2)]
        determinants = np.asarray(determinants)
        return (determinants > 0).all()

