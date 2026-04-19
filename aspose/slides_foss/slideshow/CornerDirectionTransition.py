from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .ICornerDirectionTransition import ICornerDirectionTransition

if TYPE_CHECKING:
    from .TransitionCornerDirectionType import TransitionCornerDirectionType

class CornerDirectionTransition(TransitionValueBase, ICornerDirectionTransition):
    """Corner direction slide transition effect."""
    @property
    def direction(self) -> TransitionCornerDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionCornerDirectionType import TransitionCornerDirectionType
        from .._internal.pptx.transition_mappings import CORNER_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'lu')
            enum_val = CORNER_DIR_FROM_XML.get(xml_val, 'LeftUp')
            return TransitionCornerDirectionType(enum_val)
        return TransitionCornerDirectionType.LEFT_UP

    @direction.setter
    def direction(self, value: TransitionCornerDirectionType):
        from .._internal.pptx.transition_mappings import CORNER_DIR_TO_XML
        if self._element is not None:
            xml_val = CORNER_DIR_TO_XML.get(value.value, 'lu')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
