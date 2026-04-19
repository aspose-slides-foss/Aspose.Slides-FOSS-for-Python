from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .ISideDirectionTransition import ISideDirectionTransition

if TYPE_CHECKING:
    from .TransitionSideDirectionType import TransitionSideDirectionType

class SideDirectionTransition(TransitionValueBase, ISideDirectionTransition):
    """Side direction slide transition effect."""
    @property
    def direction(self) -> TransitionSideDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionSideDirectionType import TransitionSideDirectionType
        from .._internal.pptx.transition_mappings import SIDE_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'l')
            enum_val = SIDE_DIR_FROM_XML.get(xml_val, 'Left')
            return TransitionSideDirectionType(enum_val)
        return TransitionSideDirectionType.LEFT

    @direction.setter
    def direction(self, value: TransitionSideDirectionType):
        from .._internal.pptx.transition_mappings import SIDE_DIR_TO_XML
        if self._element is not None:
            xml_val = SIDE_DIR_TO_XML.get(value.value, 'l')
            self._element.set('dir', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
