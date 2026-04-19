from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionInOutDirectionType import TransitionInOutDirectionType

class IInOutTransition(ITransitionValueBase, ABC):
    """In-Out slide transition effect."""
    @property
    @abstractmethod
    def direction(self) -> TransitionInOutDirectionType:
        """Direction of a transition effect. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: TransitionInOutDirectionType):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...