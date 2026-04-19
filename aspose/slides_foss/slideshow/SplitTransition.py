from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .ISplitTransition import ISplitTransition

if TYPE_CHECKING:
    from ..Orientation import Orientation
    from .TransitionInOutDirectionType import TransitionInOutDirectionType

class SplitTransition(TransitionValueBase, ISplitTransition):
    """Split slide transition effect."""
    @property
    def direction(self) -> TransitionInOutDirectionType:
        """Direction of transition split. Read/write ."""
        from .TransitionInOutDirectionType import TransitionInOutDirectionType
        from .._internal.pptx.transition_mappings import IN_OUT_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'out')
            enum_val = IN_OUT_DIR_FROM_XML.get(xml_val, 'Out')
            return TransitionInOutDirectionType(enum_val)
        return TransitionInOutDirectionType.OUT

    @direction.setter
    def direction(self, value: TransitionInOutDirectionType):
        from .._internal.pptx.transition_mappings import IN_OUT_DIR_TO_XML
        if self._element is not None:
            xml_val = IN_OUT_DIR_TO_XML.get(value.value, 'out')
            self._element.set('dir', xml_val)

    @property
    def orientation(self) -> Orientation:
        """Orientation of transition split. Read/write ."""
        from ..Orientation import Orientation
        from .._internal.pptx.transition_mappings import ORIENTATION_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('orient', 'horz')
            enum_val = ORIENTATION_FROM_XML.get(xml_val, 'Horizontal')
            return Orientation(enum_val)
        return Orientation.HORIZONTAL

    @orientation.setter
    def orientation(self, value: Orientation):
        from .._internal.pptx.transition_mappings import ORIENTATION_TO_XML
        if self._element is not None:
            xml_val = ORIENTATION_TO_XML.get(value.value, 'horz')
            self._element.set('orient', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
