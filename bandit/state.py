"""
FUTURE PLANS

Encode and Decode Object State through an auto-encoder

Encoding allows compression of the object state into a lower dimensional 
representation that can recombine with genetic algorithms.

The idea is to get the minimal amount of information needed to reinstate the 
object state within a range of error, which serves as a mutation mechanism if 
using evolutionary algorithms.

The object state is everything needed to reinstate the object, which includes
the root id, temporal id, cycle, step, and steps per cycle.

The object state also contains the model parameters of the object, which is what 
influences the object's behavior in the simulation.


# To Do
- Implement the encode and decode methods in the ObjectState class
- Implement the encode_self method in the Object class
- Condense an object state into a single string, and then decode it back to the 
    original state
- This will give the ability to store the state of an object in a database and 
    easily reinstate it

#! Maybe an evolutionary approach to an auto-encoder that slowly compresses the 
#!   encoding more and more, as long as the decoding output is correct
#! Will hopefully need less and less context/information to reinstate the object 
#!   from the encoded data


#! state method that turns the state into a tensor, combine that with space input state tensor, to input into the object update method for "updating"
#! update method must log the update_time attribute of the object
#! so all requests to update come through the State class and it controls the update process of the object(s)
"""

from abc import ABC

from bandit.object import ObjectState


class State(ABC):
    """
    A class to represent the state of an object

    Attributes
    ----------
    attr_list (list):
        A list of the object state variables

    Methods
    -------
    state():
        Returns the state of the object
    encode():
        Future method to encode the object state when requested
    decode(genetics: str):
        Future method to decode the object state from a lower dimensional
        representation in the form of genetics
    """

    def __init__(self, variables: dict) -> None:
        """
        Parameters
        ----------
        variables (dict):
            A dictionary of the object state variables
        """
        self.attr_list = []
        for key, value in variables.items():
            self.attr_list.append(key)
            setattr(self, key, value)

    def state(self) -> dict:
        """
        Returns the state of the object

        Returns
        -------
        dict:
            The state of the object
        """
        return {attr: getattr(self, attr) for attr in self.attr_list}

    def encode(self) -> str:
        """
        Future method to encode the object state when requested

        Returns
        -------
        genetics (str):
            A lower dimensional representation of the object state
        """
        pass

    def decode(self, genetics: str) -> "ObjectState":
        """
        Future method to decode the object state from a lower dimensional
        representation in the form of genetics

        Parameters
        ----------
        genetics (str):
            A lower dimensional representation of the object state

        Returns
        -------
        ObjectState:
            A new object state object with the decoded state
        """
        pass


class ObjectState(State):
    """
    A class to represent the state of an object

    Attributes
    ----------
    root_id (str):
        The root id of the object
    temporal_id (str):
        The temporal id of the object
    cycle (int):
        The cycle of the object
    step (int):
        The step of the object
    steps_per_cycle (int):
        The number of steps per cycle

    Methods
    -------
    state():
        Returns the state of the object
    """

    def __init__(
        self,
        root_id: str,
        temporal_id: str,
        cycle: int,
        step: int,
        steps_per_cycle: int,
    ) -> None:
        """
        Parameters
        ----------
        root_id (str):
            The root id of the object
        temporal_id (str):
            The temporal id of the object
        cycle (int):
            The cycle of the object
        step (int):
            The step of the object
        steps_per_cycle (int):
            The number of steps per cycle
        """
        super().__init__()
        self.root_id = root_id
        self.temporal_id = temporal_id
        self.cycle = cycle
        self.step = step
        self.steps_per_cycle = steps_per_cycle



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        
#! Is node the object state? or point in time? neither?

class TemporalStates:
    def __init__(self, size):
        self.size = size
        self.head = None
        self.tail = None
        self.count = 0

    def append(self, data):
        new_node = Node(data)
        if self.count < self.size:
            if self.tail is None:
                self.head = self.tail = new_node
                self.head.next = self.head
                self.head.prev = self.head
            else:
                new_node.prev = self.tail
                new_node.next = self.head
                self.tail.next = new_node
                self.head.prev = new_node
                self.tail = new_node
            self.count += 1
        else:
            new_node.prev = self.tail
            new_node.next = self.head.next
            self.head.next.prev = new_node
            self.tail.next = new_node
            self.head = self.head.next
            self.tail = new_node

    def get_last_n_states(self, n):
        if n > self.count:
            n = self.count
        current = self.tail
        states = []
        while n > 0:
            states.append(current.data)
            current = current.prev
            n -= 1
        return states[::-1]

# Example usage
state_list = CircularBuffer(3)
state_list.append("State 1")
state_list.append("State 2")
state_list.append("State 3")
state_list.append("State 4")  # Overwrites "State 1"

print(state_list.get_last_n_states(2))  # Output: ['State 3', 'State 4']


