"""
An object is a core element of TimeBandit, functioning as a specialized node 
within the simulation that maintains and updates its state.

The Object class is designed to encapsulate the object's state and its update 
method, existing within a defined Space and anchored at a specific Point in Time.

By interconnecting with other agents within the same space, objects can model 
a wide range of phenomena, such as weather patterns, population growth, city 
traffic flow, and the spread of diseases, among others.

This design allows for a rich and dynamic representation of complex systems 
through the interactions and relationships between objects.

TODO
----
- Finalize update() logic order
"""

import pickle
from abc import abstractmethod

from anarchy import Anarchy
from temporal import TemporalObject

from bandit.clock import Clock
from bandit.identity import Identity


class Object(TemporalObject):
    """
    A class to represent an object in a simulation.

    Any child class of Object must implement the _update method which contains
    the custom update logic for that object.

    During the primary update process, the object will automatically update the
    clock and the temporal_id.

    Attributes
    ----------
    step_size (int):
        The number of steps per cycle. For example, if step_size is 5, a cycle
        is counted every 5 steps.
    clock (Clock):
        The clock of the object, contains the relative time of the object in
        cycles and steps
    id (Identity):
        The identity of the object including root and temporal IDs
    state ():
        Includes the current state of the object

    Methods
    -------
    _update():
        Custom update method
    update() -> State:
        Updates the object state and returns the state after the update.
    _record_state() -> State:
        Returns the current state of the object
    save(path: str) -> str:
        Pickle object to file, saved to path/root_id
    load(path: str) -> "Object":
        Load object from file

    Properties
    ----------
    cycle: int
        Returns the cycle of the object
    step: int
        Returns the step of the object
    """

    def __init__(self, step_size: int = 1) -> None:
        """
        Parameters
        ----------
        steps_per_cycle (int):
            The number of steps per cycle
        """
        super().__init__()
        self.step_size = step_size
        self.clock = Clock(step_size)
        self.id = Identity()
        self.connections = Anarchy(anarchy_name="connections")
        self.interactions = Anarchy(anarchy_name="interactions")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.id.root}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:{self.id.root}"

    @abstractmethod
    def _update(self) -> dict:
        """
        Updates the object state and returns the state after the update.
        """
        raise NotImplementedError("Subclass must implement _update method")

    def update(self) -> dict:
        """
        Updates the object state and returns the state after the update.

        Updates the clock and the temporal_id.

        Returns
        -------
        dict:
            The state of the object

        TODO
        ----
        - Finalize update() logic order
        """
        self._update()
        self.clock.update()
        self.id.update(self.clock)

        return super().update(self.state(), self.id.temporal)

    def save(self, path: str) -> str:
        """
        Pickle object to file, saved to path/root_id
        """
        try:
            full_path = f"{path}/{self.id.root}"
            with open(full_path, "wb") as f:
                pickle.dump(self, f)
            return full_path
        except Exception as e:
            # Handle exceptions and log errors
            print(f"Failed to save object: {e}")
            return ""

    @classmethod
    def load(cls, path: str) -> "Object":
        """
        Load object from file
        """
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
            return obj
        except Exception as e:
            # Handle exceptions and log errors
            print(f"Failed to load object: {e}")
            return ""

    @abstractmethod
    def state(self):
        """
        Returns the state of the object
        """
        return {
            "step_size": self.step_size,
            "root_id": self.id.root,
            "temporal_id": self.id.temporal,
            "cycle": self.clock.cycle,
            "step": self.clock.step,
        }

    @property
    def cycle(self) -> int:
        """
        Returns the relative cycle of the object
        """
        return self.clock.cycle

    @property
    def step(self) -> int:
        """
        Returns the relative step of the object
        """
        return self.clock.step
