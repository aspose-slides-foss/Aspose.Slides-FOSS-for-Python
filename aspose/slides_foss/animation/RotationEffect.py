from __future__ import annotations
from typing import TYPE_CHECKING
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IRotationEffect import IRotationEffect

if TYPE_CHECKING:
    from ..NullableBool import NullableBool
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming


class RotationEffect(Behavior, IRotationEffect):
    """Represent rotation effect behavior of effect."""

    def __init__(self):
        ...

    @property
    def from_address(self) -> float:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('from')
            if val is not None:
                return float(val)
        return 0.0

    @from_address.setter
    def from_address(self, value: float):
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('from', str(value))

    @property
    def to(self) -> float:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('to')
            if val is not None:
                return float(val)
        return 0.0

    @to.setter
    def to(self, value: float):
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('to', str(value))

    @property
    def by(self) -> float:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('by')
            if val is not None:
                return float(val)
        return 0.0

    @by.setter
    def by(self, value: float):
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('by', str(value))

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
