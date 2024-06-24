"""
Graph class is a abstract class that represents a graph.

It is a subclass of networkx.DiGraph.

A graph is a collection of nodes and edges. The nodes are the objects in the graph
and the edges are the relationships between the objects.

It is intended to be subclassed by concrete implementations of graphs. Like
the Space class and the Time class.
    
TODO
----
- Better state management to auto use parent state details so dont have to 
    define with every child
- Decide if Space should inherit from Object
"""

from abc import abstractmethod
from typing import TYPE_CHECKING

import networkx as nx

from bandit.state import TemporalState

if TYPE_CHECKING:
    from bandit.object import Object


class Graph(nx.DiGraph):
    """
    Graph class is a abstract class that represents a graph.

    It is a subclass of networkx.DiGraph.

    It is intended to be subclassed by concrete implementations of graphs. Like
    the Space class and the Time class.

    Methods
    -------
    add_object(object):
        Adds an object to the space
    remove_object(object):
        Removes an object from the space
    get_object(object_id):
        Returns the object
    draw_space():
        Draws the space
    update(input):
        Updates the object state
    draw():
        Draws the graph
    state():
        Returns the state of the graph
    """

    #! Should Space just inherit from Object?
    def __init__(self) -> None:
        super().__init__()
        self.object_states = {}
        self.state = TemporalState()

    def add_object(self, object) -> None:
        """
        Adds an object to the space

        Parameters
        ----------
        object (Object):
            The object to add to the space
        """
        self.add_node(object.root_id, object=object)

    def remove_object(self, object) -> None:
        """
        Removes an object from the space

        Parameters
        ----------
        object (Object):
            The object to remove from the space
        """
        self.remove_node(object)

    def get_object(self, object_id) -> "Object":
        """
        Returns the object

        Parameters
        ----------
        object_id (str):
            The id of the object

        Returns
        -------
        Object:
            The object
        """
        return self.nodes[object_id]["object"]

    @abstractmethod
    def _update(self) -> None:
        """
        Updates the object state
        """
        raise NotImplementedError("Subclass must implement _update")

    def update(self) -> dict:
        """
        Updates the object state

        - Iter through every object
        - Update the object
        - Return the state of the object
        - Insert into temporal graph
        - Connect the threads between current state and previous state
        - Finalize update
        - Return the state of the object
        """
        self.object_states = {}
        for object in self.objects:
            # Update every object in the graph
            self.object_states[object.root_id] = object.update()

        return self.state

    def draw(self) -> None:
        """
        Draws the graph
        """
        nx.draw(self, with_labels=True, font_weight="bold")

    @property
    def objects(self) -> dict:
        """
        Returns the objects in the graph
        """
        for node in self.nodes():
            yield self.nodes[node]["object"]

    @property
    def state(self) -> dict:
        """
        Returns the state of the graph
        """
        return {
            "object_count": len(self.object_states),
            "object_states": self.object_states,
        }
