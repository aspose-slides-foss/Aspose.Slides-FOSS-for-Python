from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionLeftRightDirectionType import TransitionLeftRightDirectionType

class ILeftRightDirectionTransition(ITransitionValueBase, ABC):
    """Left-right direction slide transition effect."""
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
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...