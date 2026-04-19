from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IColorEffect import IColorEffect

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool
    from ..IColorFormat import IColorFormat
    from .IColorOffset import IColorOffset
    from .ColorSpace import ColorSpace
    from .ColorDirection import ColorDirection


class ColorEffect(Behavior, IColorEffect):
    """Represent color effect behavior of effect."""

    def __init__(self):
        self._from = None
        self._to = None
        self._by = None
        self._color_space_val = None
        self._direction_val = None

    @property
    def from_address(self) -> IColorFormat:
        return self._from

    @from_address.setter
    def from_address(self, value: IColorFormat):
        self._from = value

    @property
    def to(self) -> IColorFormat:
        return self._to

    @to.setter
    def to(self, value: IColorFormat):
        self._to = value

    @property
    def by(self) -> IColorOffset:
        return self._by

    @by.setter
    def by(self, value: IColorOffset):
        self._by = value

    @property
    def color_space(self) -> ColorSpace:
        from .ColorSpace import ColorSpace
        if self._color_space_val is not None:
            return self._color_space_val
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('clrSpc')
            _map = {'rgb': ColorSpace.RGB, 'hsl': ColorSpace.HSL}
            return _map.get(val, ColorSpace.NOT_DEFINED)
        return ColorSpace.NOT_DEFINED

    @color_space.setter
    def color_space(self, value: ColorSpace):
        self._color_space_val = value

    @property
    def direction(self) -> ColorDirection:
        from .ColorDirection import ColorDirection
        if self._direction_val is not None:
            return self._direction_val
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('dir')
            _map = {'cw': ColorDirection.CLOCKWISE, 'ccw': ColorDirection.COUNTER_CLOCKWISE}
            return _map.get(val, ColorDirection.NOT_DEFINED)
        return ColorDirection.NOT_DEFINED

    @direction.setter
    def direction(self, value: ColorDirection):
        self._direction_val = value

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
