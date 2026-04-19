from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IEightDirectionTransition import IEightDirectionTransition

if TYPE_CHECKING:
    from .TransitionEightDirectionType import TransitionEightDirectionType

class EightDirectionTransition(TransitionValueBase, IEightDirectionTransition):
    """Eight direction slide transition effect."""
    @property
    def direction(self) -> TransitionEightDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionEightDirectionType import TransitionEightDirectionType
        from .._internal.pptx.transition_mappings import EIGHT_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'l')
            enum_val = EIGHT_DIR_FROM_XML.get(xml_val, 'Left')
            return TransitionEightDirectionType(enum_val)
        return TransitionEightDirectionType.LEFT

    @direction.setter
    def direction(self, value: TransitionEightDirectionType):
        from .._internal.pptx.transition_mappings import EIGHT_DIR_TO_XML
        if self._element is not None:
            xml_val = EIGHT_DIR_TO_XML.get(value.value, 'l')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
