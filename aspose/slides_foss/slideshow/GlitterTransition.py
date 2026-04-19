from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IGlitterTransition import IGlitterTransition

if TYPE_CHECKING:
    from .TransitionPattern import TransitionPattern
    from .TransitionSideDirectionType import TransitionSideDirectionType

class GlitterTransition(TransitionValueBase, IGlitterTransition):
    """Glitter slide transition effect."""
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
    def pattern(self) -> TransitionPattern:
        """Specifies the shape of the visuals used during the transition. Read/write ."""
        from .TransitionPattern import TransitionPattern
        from .._internal.pptx.transition_mappings import PATTERN_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('pattern', 'diamond')
            enum_val = PATTERN_FROM_XML.get(xml_val, 'Diamond')
            return TransitionPattern(enum_val)
        return TransitionPattern.DIAMOND

    @pattern.setter
    def pattern(self, value: TransitionPattern):
        from .._internal.pptx.transition_mappings import PATTERN_TO_XML
        if self._element is not None:
            xml_val = PATTERN_TO_XML.get(value.value, 'diamond')
            self._element.set('pattern', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
