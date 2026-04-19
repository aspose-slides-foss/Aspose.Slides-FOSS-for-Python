from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionInOutDirectionType import TransitionInOutDirectionType

class IFlyThroughTransition(ITransitionValueBase, ABC):
    """Fly-through slide transition effect."""
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
    def has_bounce(self) -> bool:
        """Specifies that the movement of the presentation slides during the transition includes a bounce. Read/write ."""
        ...
    @has_bounce.setter
    @abstractmethod
    def has_bounce(self, value: bool):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...