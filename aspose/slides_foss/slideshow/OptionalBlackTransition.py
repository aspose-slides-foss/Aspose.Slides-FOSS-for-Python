from __future__ import annotations
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IOptionalBlackTransition import IOptionalBlackTransition

class OptionalBlackTransition(TransitionValueBase, IOptionalBlackTransition):
    """Optional black slide transition effect."""
    @property
    def from_black(self) -> bool:
        """This attribute specifies if the transition will start from a black screen (and then transition the new slide over black). Read/write ."""
        if self._element is not None:
            return self._element.get('thruBlk', '0') == '1'
        return False

    @from_black.setter
    def from_black(self, value: bool):
        if self._element is not None:
            if value:
                self._element.set('thruBlk', '1')
            elif 'thruBlk' in self._element.attrib:
                del self._element.attrib['thruBlk']

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
