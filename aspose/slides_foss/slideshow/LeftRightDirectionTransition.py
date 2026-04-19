from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .ILeftRightDirectionTransition import ILeftRightDirectionTransition

if TYPE_CHECKING:
    from .TransitionLeftRightDirectionType import TransitionLeftRightDirectionType

class LeftRightDirectionTransition(TransitionValueBase, ILeftRightDirectionTransition):
    """Left-right direction slide transition effect."""
    @property
    def direction(self) -> TransitionLeftRightDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionLeftRightDirectionType import TransitionLeftRightDirectionType
        from .._internal.pptx.transition_mappings import LEFT_RIGHT_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'l')
            enum_val = LEFT_RIGHT_DIR_FROM_XML.get(xml_val, 'Left')
            return TransitionLeftRightDirectionType(enum_val)
        return TransitionLeftRightDirectionType.LEFT

    @direction.setter
    def direction(self, value: TransitionLeftRightDirectionType):
        from .._internal.pptx.transition_mappings import LEFT_RIGHT_DIR_TO_XML
        if self._element is not None:
            xml_val = LEFT_RIGHT_DIR_TO_XML.get(value.value, 'l')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
