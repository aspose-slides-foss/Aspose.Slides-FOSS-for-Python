from __future__ import annotations
from typing import TYPE_CHECKING
from .TransitionValueBase import TransitionValueBase
from .ITransitionValueBase import ITransitionValueBase
from .IFlyThroughTransition import IFlyThroughTransition

if TYPE_CHECKING:
    from .TransitionInOutDirectionType import TransitionInOutDirectionType

class FlyThroughTransition(TransitionValueBase, IFlyThroughTransition):
    """Fly-through slide transition effect."""
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
    def has_bounce(self) -> bool:
        """Specifies that the movement of the presentation slides during the transition includes a bounce. Read/write ."""
        if self._element is not None:
            return self._element.get('hasBounce', '0') == '1'
        return False

    @has_bounce.setter
    def has_bounce(self, value: bool):
        if self._element is not None:
            if value:
                self._element.set('hasBounce', '1')
            elif 'hasBounce' in self._element.attrib:
                del self._element.attrib['hasBounce']

    @property
    def as_i_transition_value_base(self) -> ITransitionValueBase:
        return self
