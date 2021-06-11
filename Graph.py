from Node import Node
from collections import defaultdict


class Graph:
    def __init__(self):
        self.name = str
        self.Adj = defaultdict(list)
        self.nodes = defaultdict(Node)

    def set_name(self, string):
        self.name = string

    def get_name(self):
        return self.name

    def is_edge(self, u, v) -> bool:
        if v in self.Adj[u]:
            return True
        return False

    def add_edge(self, u, v):
        self.Adj[u].append(v)
        self.nodes[u].set_val(u)
        self.nodes[v].set_val(v)

    def get_adj(self):
        return self.Adj

    def get_nodes(self):
        return self.nodes

    def add_node(self, node):
        if self.nodes.get(node) is None:
            self.nodes[node].set_val(node)
            self.Adj[node] = []

    def send_str(self):
        s = ''
        for u in self.Adj.keys():
            neighbors = self.Adj[u]
            for v in neighbors:
                s += "({0},{1})\n".format(u, v)
        return s



