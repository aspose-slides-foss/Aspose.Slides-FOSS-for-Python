from __future__ import annotations
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IEmptyTransition import IEmptyTransition

class EmptyTransition(TransitionValueBase, IEmptyTransition):
    """Empty slide transition effect."""
    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
