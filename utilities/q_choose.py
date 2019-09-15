
def n_q(n, q):
    return (q ** n - 1) / (q - 1)


def q_choose(n, k, q):
    result = 1
    for i in range(n, n-k, -1):
        result *= n_q(i, q)

    for i in range(k, 1, -1):
        result /= n_q(i, q)

    return result
