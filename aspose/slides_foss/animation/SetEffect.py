from __future__ import annotations
from typing import TYPE_CHECKING, Any
import lxml.etree as ET
from .Behavior import Behavior
from .IBehavior import IBehavior
from .ISetEffect import ISetEffect
from .._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool


class SetEffect(Behavior, ISetEffect):
    """Represent set effect behavior of effect."""

    def __init__(self):
        ...

    @property
    def to(self) -> object:
        to_elem = self._elem.find(Elements.P_TO)
        if to_elem is not None:
            str_val = to_elem.find(Elements.P_STR_VAL)
            if str_val is not None:
                return str_val.get('val')
        return None

    @to.setter
    def to(self, value: object):
        to_elem = self._elem.find(Elements.P_TO)
        if to_elem is None:
            to_elem = ET.SubElement(self._elem, Elements.P_TO)
        str_val = to_elem.find(Elements.P_STR_VAL)
        if str_val is None:
            str_val = ET.SubElement(to_elem, Elements.P_STR_VAL)
        str_val.set('val', str(value))

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
