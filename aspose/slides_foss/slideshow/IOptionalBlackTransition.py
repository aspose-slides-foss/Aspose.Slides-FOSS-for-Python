from __future__ import annotations
from abc import ABC, abstractmethod
from .ITransitionValueBase import ITransitionValueBase

class IOptionalBlackTransition(ITransitionValueBase, ABC):
    """Optional black slide transition effect."""
    @property
    @abstractmethod
    def from_black(self) -> bool:
        """This attribute specifies if the transition will start from a black screen (and then transition the new slide over black). Read/write ."""
        ...
    @from_black.setter
    @abstractmethod
    def from_black(self, value: bool):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...