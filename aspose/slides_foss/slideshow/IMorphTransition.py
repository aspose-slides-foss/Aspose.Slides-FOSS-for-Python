from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITransitionValueBase import ITransitionValueBase

if TYPE_CHECKING:
    from .TransitionMorphType import TransitionMorphType

class IMorphTransition(ITransitionValueBase, ABC):
    """Ripple slide transition effect."""
    @property
    @abstractmethod
    def morph_type(self) -> TransitionMorphType:
        """Type of morph transition. Read/write ."""
        ...
    @morph_type.setter
    @abstractmethod
    def morph_type(self, value: TransitionMorphType):
        ...
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...