from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IScaleEffect import IScaleEffect

if TYPE_CHECKING:
    from ..NullableBool import NullableBool
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming


class ScaleEffect(Behavior, IScaleEffect):
    """Represent scale effect behavior of effect."""

    def __init__(self):
        ...

    @property
    def zoom_content(self) -> NullableBool:
        from ..NullableBool import NullableBool
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('zoomContents')
            if val == '1':
                return NullableBool.TRUE
            if val == '0':
                return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @zoom_content.setter
    def zoom_content(self, value: NullableBool):
        from ..NullableBool import NullableBool
        if hasattr(self, '_elem') and self._elem is not None:
            if value == NullableBool.TRUE:
                self._elem.set('zoomContents', '1')
            elif value == NullableBool.FALSE:
                self._elem.set('zoomContents', '0')

    @property
    def from_address(self) -> Any:
        return None

    @from_address.setter
    def from_address(self, value: Any):
        pass

    @property
    def to(self) -> Any:
        return None

    @to.setter
    def to(self, value: Any):
        pass

    @property
    def by(self) -> Any:
        return None

    @by.setter
    def by(self, value: Any):
        pass

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
