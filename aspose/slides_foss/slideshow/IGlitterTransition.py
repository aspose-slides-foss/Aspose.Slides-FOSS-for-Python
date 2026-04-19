from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionPattern import TransitionPattern
    from .TransitionSideDirectionType import TransitionSideDirectionType

class IGlitterTransition(ITransitionValueBase, ABC):
    """Glitter slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> TransitionSideDirectionType:
        """Direction of transition. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: TransitionSideDirectionType):
        ...
    @property
    @abstractmethod
    def pattern(self) -> TransitionPattern:
        """Specifies the shape of the visuals used during the transition. Read/write ."""
        ...
    @pattern.setter
    @abstractmethod
    def pattern(self, value: TransitionPattern):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...