from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionLeftRightDirectionType import TransitionLeftRightDirectionType

class IRevealTransition(ITransitionValueBase, ABC):
    """Reveal slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> TransitionLeftRightDirectionType:
        """Direction of transition. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: TransitionLeftRightDirectionType):
        ...
    @property
    @abstractmethod
    def through_black(self) -> bool:
        """Specifies whether the transition fades through black. Read/write ."""
        ...
    @through_black.setter
    @abstractmethod
    def through_black(self, value: bool):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...