from __future__ import annotations
from abc import ABC, abstractmethod
from .ITransitionValueBase import ITransitionValueBase

class IWheelTransition(ITransitionValueBase, ABC):
    """Wheel slide transition effect."""
    @property
    @abstractmethod
    def spokes(self) -> int:
        """Number spokes of wheel transition. Read/write ."""
        ...
    @spokes.setter
    @abstractmethod
    def spokes(self, value: int):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...