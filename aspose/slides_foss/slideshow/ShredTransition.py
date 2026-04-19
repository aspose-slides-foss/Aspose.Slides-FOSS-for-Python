from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IShredTransition import IShredTransition

if TYPE_CHECKING:
    from .TransitionInOutDirectionType import TransitionInOutDirectionType
    from .TransitionShredPattern import TransitionShredPattern

class ShredTransition(TransitionValueBase, IShredTransition):
    """Shred slide transition effect."""
    @property
    def direction(self) -> TransitionInOutDirectionType:
        """Direction of transition. Read/write ."""
        from .TransitionInOutDirectionType import TransitionInOutDirectionType
        from .._internal.pptx.transition_mappings import IN_OUT_DIR_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('dir', 'in')
            enum_val = IN_OUT_DIR_FROM_XML.get(xml_val, 'In')
            return TransitionInOutDirectionType(enum_val)
        return TransitionInOutDirectionType.IN

    @direction.setter
    def direction(self, value: TransitionInOutDirectionType):
        from .._internal.pptx.transition_mappings import IN_OUT_DIR_TO_XML
        if self._element is not None:
            xml_val = IN_OUT_DIR_TO_XML.get(value.value, 'in')
            self._element.set('dir', xml_val)

    @property
    def pattern(self) -> TransitionShredPattern:
        """Specifies the shape of the visuals used during the transition. Read/write ."""
        from .TransitionShredPattern import TransitionShredPattern
        from .._internal.pptx.transition_mappings import SHRED_PATTERN_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('pattern', 'strip')
            enum_val = SHRED_PATTERN_FROM_XML.get(xml_val, 'Strip')
            return TransitionShredPattern(enum_val)
        return TransitionShredPattern.STRIP

    @pattern.setter
    def pattern(self, value: TransitionShredPattern):
        from .._internal.pptx.transition_mappings import SHRED_PATTERN_TO_XML
        if self._element is not None:
            xml_val = SHRED_PATTERN_TO_XML.get(value.value, 'strip')
            self._element.set('pattern', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
