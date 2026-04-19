from __future__ import annotations
from abc import ABC, abstractmethod
from .ITransitionValueBase import ITransitionValueBase

class IEmptyTransition(ITransitionValueBase, ABC):
    """Empty slide transition effect."""
    @property
    @abstractmethod
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        """Allows to get base ITransitionValueBase interface. Read-only ."""
        ...