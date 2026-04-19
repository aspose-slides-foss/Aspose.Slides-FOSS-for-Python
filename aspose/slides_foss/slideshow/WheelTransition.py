from __future__ import annotations
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IWheelTransition import IWheelTransition

class WheelTransition(TransitionValueBase, IWheelTransition):
    """Wheel slide transition effect."""
    @property
    def spokes(self) -> int:
        """Number spokes of wheel transition. Read/write ."""
        if self._element is not None:
            return int(self._element.get('spokes', '4'))
        return 4

    @spokes.setter
    def spokes(self, value: int):
        if self._element is not None:
            self._element.set('spokes', str(value))

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
