import networkx as nx

from bandit.graph import Graph


class Space(Graph):
    """
    Space class is a directed graph that represents the space of objects.
    It is a subclass of networkx.DiGraph.
    """

    def __init__(self):
        super().__init__()