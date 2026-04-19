from __future__ import annotations
from typing import TYPE_CHECKING
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IPropertyEffect import IPropertyEffect

if TYPE_CHECKING:
    from ..NullableBool import NullableBool
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .IPointCollection import IPointCollection
    from .ITiming import ITiming
    from .PropertyCalcModeType import PropertyCalcModeType
    from .PropertyValueType import PropertyValueType


class PropertyEffect(Behavior, IPropertyEffect):
    """Represent property effect behavior of effect."""

    def __init__(self):
        self._from_val = None
        self._to_val = None
        self._by_val = None
        self._value_type_val = None
        self._calc_mode_val = None
        self._points_val = None

    @property
    def from_address(self) -> str:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('from')
            if val is not None:
                return val
        return self._from_val or ''

    @from_address.setter
    def from_address(self, value: str):
        self._from_val = value
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('from', str(value))

    @property
    def to(self) -> str:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('to')
            if val is not None:
                return val
        return self._to_val or ''

    @to.setter
    def to(self, value: str):
        self._to_val = value
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('to', str(value))

    @property
    def by(self) -> str:
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('by')
            if val is not None:
                return val
        return self._by_val or ''

    @by.setter
    def by(self, value: str):
        self._by_val = value

    @property
    def value_type(self) -> PropertyValueType:
        from .PropertyValueType import PropertyValueType
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('valueType')
            _map = {'str': PropertyValueType.STRING, 'num': PropertyValueType.NUMBER, 'clr': PropertyValueType.COLOR}
            return _map.get(val, PropertyValueType.NOT_DEFINED)
        return self._value_type_val or PropertyValueType.NOT_DEFINED

    @value_type.setter
    def value_type(self, value: PropertyValueType):
        self._value_type_val = value

    @property
    def calc_mode(self) -> PropertyCalcModeType:
        from .PropertyCalcModeType import PropertyCalcModeType
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('calcmode')
            _map = {'discrete': PropertyCalcModeType.DISCRETE, 'lin': PropertyCalcModeType.LINEAR, 'fmla': PropertyCalcModeType.FORMULA}
            return _map.get(val, PropertyCalcModeType.NOT_DEFINED)
        return self._calc_mode_val or PropertyCalcModeType.NOT_DEFINED

    @calc_mode.setter
    def calc_mode(self, value: PropertyCalcModeType):
        self._calc_mode_val = value

    @property
    def points(self) -> IPointCollection:
        return self._points_val

    @points.setter
    def points(self, value: IPointCollection):
        self._points_val = value

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
