from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IMorphTransition import IMorphTransition

if TYPE_CHECKING:
    from .TransitionMorphType import TransitionMorphType

class MorphTransition(TransitionValueBase, IMorphTransition):
    """Morph slide transition effect."""
    @property
    def morph_type(self) -> TransitionMorphType:
        """Type of morph transition. Read/write ."""
        from .TransitionMorphType import TransitionMorphType
        from .._internal.pptx.transition_mappings import MORPH_TYPE_FROM_XML
        if self._element is not None:
            xml_val = self._element.get('option', 'byObject')
            enum_val = MORPH_TYPE_FROM_XML.get(xml_val, 'ByObject')
            return TransitionMorphType(enum_val)
        return TransitionMorphType.BY_OBJECT

    @morph_type.setter
    def morph_type(self, value: TransitionMorphType):
        from .._internal.pptx.transition_mappings import MORPH_TYPE_TO_XML
        if self._element is not None:
            xml_val = MORPH_TYPE_TO_XML.get(value.value, 'byObject')
            self._element.set('option', xml_val)

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
