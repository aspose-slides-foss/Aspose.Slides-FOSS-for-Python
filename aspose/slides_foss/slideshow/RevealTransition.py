from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IRevealTransition import IRevealTransition

if TYPE_CHECKING:
    from .TransitionLeftRightDirectionType import TransitionLeftRightDirectionType

class RevealTransition(TransitionValueBase, IRevealTransition):
    """Reveal slide transition effect."""
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
    def through_black(self) -> bool:
        """Specifies whether the transition fades through black. Read/write ."""
        if self._element is not None:
            return self._element.get('thruBlk', '0') == '1'
        return False

    @through_black.setter
    def through_black(self, value: bool):
        if self._element is not None:
            if value:
                self._element.set('thruBlk', '1')
            elif 'thruBlk' in self._element.attrib:
                del self._element.attrib['thruBlk']

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
