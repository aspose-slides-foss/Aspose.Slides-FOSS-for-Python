from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from ..Orientation import Orientation

class IOrientationTransition(ITransitionValueBase, ABC):
    """Orientation slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> Orientation:
        """Direction of transition. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: Orientation):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...