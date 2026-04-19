from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from ..Orientation import Orientation
    from .TransitionInOutDirectionType import TransitionInOutDirectionType

class ISplitTransition(ITransitionValueBase, ABC):
    """Split slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> TransitionInOutDirectionType:
        """Direction of transition split. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: TransitionInOutDirectionType):
        ...
    @property
    @abstractmethod
    def orientation(self) -> Orientation:
        """Orientation of transition split. Read/write ."""
        ...
    @orientation.setter
    @abstractmethod
    def orientation(self, value: Orientation):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...