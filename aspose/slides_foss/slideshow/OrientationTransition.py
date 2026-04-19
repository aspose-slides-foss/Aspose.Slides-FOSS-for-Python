from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IOrientationTransition import IOrientationTransition

if TYPE_CHECKING:
    from ..Orientation import Orientation

class OrientationTransition(TransitionValueBase, IOrientationTransition):
    """Orientation slide transition effect."""
    @property
    def direction(self) -> Orientation:
        """Direction of transition. Read/write ."""
        from ..Orientation import Orientation
        from .._internal.pptx.transition_mappings import ORIENTATION_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'horz')
            enum_val = ORIENTATION_FROM_XML.get(xml_val, 'Horizontal')
            return Orientation(enum_val)
        return Orientation.HORIZONTAL

    @direction.setter
    def direction(self, value: Orientation):
        from .._internal.pptx.transition_mappings import ORIENTATION_TO_XML
        if self._element is not None:
            xml_val = ORIENTATION_TO_XML.get(value.value, 'horz')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
