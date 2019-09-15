from itertools import product
import networkx as nx


def special_3_regular():
    graph = nx.Graph()
    graph.add_nodes_from(product(range(5), range(3)))
    graph.add_node(0)
    for j in range(3):
        graph.add_cycle(product(range(5), [j]))
        graph.add_edges_from([((1, j), (3, j)), ((2, j), (4, j))])
        graph.add_edge(0, (0, j))
    return nx.convert_node_labels_to_integers(graph)

