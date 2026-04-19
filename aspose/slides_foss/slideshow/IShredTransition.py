from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionInOutDirectionType import TransitionInOutDirectionType
    from .TransitionShredPattern import TransitionShredPattern

class IShredTransition(ITransitionValueBase, ABC):
    """Shred slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> TransitionInOutDirectionType:
        """Direction of transition. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: TransitionInOutDirectionType):
        ...
    @property
    @abstractmethod
    def pattern(self) -> TransitionShredPattern:
        """Specifies the shape of the visuals used during the transition. Read/write ."""
        ...
    @pattern.setter
    @abstractmethod
    def pattern(self, value: TransitionShredPattern):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...