import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


class OrientedLabelledGraphWithBasePoint:
    _LABEL = 'label'

    def __init__(self):
        self._graph = nx.MultiDiGraph()
        self._graph.add_node(0)

    @classmethod
    def _from_graph(cls, graph):
        result = cls()
        edges = list(graph.edges(keys=True, data=True))
        for edge in edges:
            label = edge[3][cls._LABEL]
            if edge[0] > edge[1] or edge[0] == edge[1] and label.ext_rep[1] < 0:
                graph.remove_edge(edge[0], edge[1], key=edge[2])
                graph.add_edge(edge[1], edge[0], label=label.inverse())
        result._graph = graph
        return result

    def copy(self):
        return OrientedLabelledGraphWithBasePoint._from_graph(self._graph)

    @staticmethod
    def base_point():
        return 0

    def __len__(self):
        return len(self._graph)

    def nodes(self):
        return self._graph.nodes

    def number_of_nodes(self):
        return len(self._graph.nodes)

    def positive_edges(self, nodes=None):
        edges = self._graph.out_edges(nbunch=nodes, keys=True, data=True)
        return [(x[0], x[1], x[2], x[3][OrientedLabelledGraphWithBasePoint._LABEL]) for x in edges]

    def edges(self, node):
        out_edges = self._graph.out_edges(nbunch=[node], keys=True, data=True)
        in_edges = self._graph.in_edges(nbunch=[node], keys=True, data=True)
        edges = [(x[0], x[1], x[2], x[3][OrientedLabelledGraphWithBasePoint._LABEL]) for x in out_edges]
        edges += [(x[1], x[0], x[2], x[3][OrientedLabelledGraphWithBasePoint._LABEL].inverse()) for x in in_edges]
        return edges

    def edge_label(self, u, v, n):
        if u > v:
            return self.edge_label(v, u, n).inverse()
        return self._graph.adj[u][v][n]['label']

    def has_edge(self, u, v):
        if u > v:
            return self.has_edge(v, u)
        return self._graph.has_edge(u, v)

    def edge_labels(self, u, v):
        if u > v:
            labels = self.edge_labels(v, u)
            return set([label.inverse() for label in labels])
        if u not in self._graph.adj or v not in self._graph.adj[u]:
            return set()
        labels = set([self._graph.adj[u][v][n][OrientedLabelledGraphWithBasePoint._LABEL]
                      for n in self._graph.adj[u][v]])
        if u == v:
            return set([label if label.ext_rep[1] > 0 else label.inverse() for label in labels])
        else:
            return labels

    def add_edge(self, u, v, label):
        if u > v:
            self.add_edge(v, u, label.inverse())
            return
        if u == v and label.ext_rep[1] < 0:
            self.add_edge(u, v, label.inverse())
        self._graph.add_edge(u, v, label=label)

    def remove_all_edges(self, u, v):
        if u > v:
            self.remove_all_edges(v, u)
            return
        if self._graph.number_of_edges(u, v) == 0:
            return
        edge_keys = list(self._graph.adj[u][v].keys())
        for n in edge_keys:
            self.remove_edge(u, v, n)

    def remove_edge(self, u, v, n):
        if u > v:
            self.remove_edge(v, u, n)
            return
        self._graph.remove_edge(u, v, n)

    def add_node(self, node):
        self._graph.add_node(node)

    def fold(self):
        graph = self.copy()
        found = True
        while found:
            found = False
            for node in graph.nodes():
                edges = graph.edges(node)

                for edge_pair in combinations(edges, r=2):
                    if edge_pair[0][3] == edge_pair[1][3]:
                        edges_to_fold = edge_pair
                        found = True
                        break
                if found:
                    break
            if found:
                graph = graph.fold_graph_edges(edges_to_fold[0], edges_to_fold[1])
        return graph

    def fold_graph_edges(self, edge1, edge2):
        if edge1[0] == edge2[0]:
            u = edge1[1]
            v = edge2[1]
        else:
            u = edge1[0]
            v = edge2[0]
        if u == v:
            u = edge1[0]
            v = edge1[1]
            edges_data = self.edge_labels(u, v)
            self.remove_all_edges(u, v)
            for x in edges_data:
                self.add_edge(u, v, x)
            return self
        else:
            return self.identify_nodes(u, v)

    def identify_nodes(self, u, v):
        if u > v:
            return self.identify_nodes(v, u)
        elif u == v:
            return self
        edges_data = self.edge_labels(u, v)
        edges_data = edges_data.union(self.edge_labels(u, u))
        edges_data = edges_data.union(self.edge_labels(v, v))

        new_graph = nx.identified_nodes(self._graph, u, v, self_loops=False)
        graph = OrientedLabelledGraphWithBasePoint._from_graph(new_graph)
        graph.remove_all_edges(u, u)
        for x in edges_data:
            graph.add_edge(u, u, x)
        return graph

    def is_isomorphic(self, other):
        def compare_edge_labels(x, y):
            x_labels = set([x[a]['label'] for a in x])
            y_labels = set([y[a]['label'] for a in y])
            return x_labels == y_labels
        return nx.is_isomorphic(self._graph, other._graph,
                                edge_match=compare_edge_labels)

    def draw(self):
        pos = nx.spring_layout(self._graph)
        labels = {}
        node_labels = {}
        for edge in self._graph.edges:
            edge_vertices = edge[:2]
            if edge_vertices not in labels:
                labels[edge_vertices] = []
            labels[edge_vertices].append(
                self._graph.adj[edge[0]][edge[1]][edge[2]][OrientedLabelledGraphWithBasePoint._LABEL]
            )

        for edge in self._graph.edges:
            edge_vertices = edge[:2]
            if edge[0] == edge[1]:
                node_labels[edge[0]] = labels[edge_vertices]

        node_colors = ['red'] + ['pink'] * (len(self._graph) - 1)
        nx.draw(self._graph, pos, edge_color='black', width=1, linewidths=1,
                node_size=500, node_color=node_colors, alpha=0.6)
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=labels)
        plt.show()
