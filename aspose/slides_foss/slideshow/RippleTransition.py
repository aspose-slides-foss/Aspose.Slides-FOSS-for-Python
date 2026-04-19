from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IRippleTransition import IRippleTransition

if TYPE_CHECKING:
    from .TransitionCornerAndCenterDirectionType import TransitionCornerAndCenterDirectionType

class RippleTransition(TransitionValueBase, IRippleTransition):
    """Ripple slide transition effect."""
    @property
    def direction(self) -> TransitionCornerAndCenterDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionCornerAndCenterDirectionType import TransitionCornerAndCenterDirectionType
        from .._internal.pptx.transition_mappings import CORNER_CENTER_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'center')
            enum_val = CORNER_CENTER_DIR_FROM_XML.get(xml_val, 'Center')
            return TransitionCornerAndCenterDirectionType(enum_val)
        return TransitionCornerAndCenterDirectionType.CENTER

    @direction.setter
    def direction(self, value: TransitionCornerAndCenterDirectionType):
        from .._internal.pptx.transition_mappings import CORNER_CENTER_DIR_TO_XML
        if self._element is not None:
            xml_val = CORNER_CENTER_DIR_TO_XML.get(value.value, 'center')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
