from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .IPointCollection import IPointCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool
    from .PropertyCalcModeType import PropertyCalcModeType
    from .PropertyValueType import PropertyValueType

class IPropertyEffect(IBehavior, ABC):
    """Represent property effect behavior."""
    @property
    @abstractmethod
    def from_address(self) -> str:
        """Specifies the starting value of the animation. Read/write ."""
        ...
    @from_address.setter
    @abstractmethod
    def from_address(self, value: str):
        ...
    @property
    @abstractmethod
    def to(self) -> str:
        """Specifies the ending value for the animation. Read/write ."""
        ...
    @to.setter
    @abstractmethod
    def to(self, value: str):
        ...
    @property
    @abstractmethod
    def by(self) -> str:
        """Specifies a relative offset value for the animation with respect to its position before the start of the animation. Read/write ."""
        ...
    @by.setter
    @abstractmethod
    def by(self, value: str):
        ...
    @property
    @abstractmethod
    def value_type(self) -> PropertyValueType:
        """Specifies the type of a property value. Read/write ."""
        ...
    @value_type.setter
    @abstractmethod
    def value_type(self, value: PropertyValueType):
        ...
    @property
    @abstractmethod
    def calc_mode(self) -> PropertyCalcModeType:
        """Specifies the interpolation mode for the animation Read/write ."""
        ...
    @calc_mode.setter
    @abstractmethod
    def calc_mode(self, value: PropertyCalcModeType):
        ...
    @property
    @abstractmethod
    def points(self) -> IPointCollection:
        """Specifies the points of the animation. Read/write ."""
        ...
    @points.setter
    @abstractmethod
    def points(self, value: IPointCollection):
        ...
    @property
    @abstractmethod
    def as_i_behavior(self) -> IBehavior:
        """Allows to get base IBehavior interface. Read-only ."""
        ...
    @property
    @abstractmethod
    def accumulate(self) -> NullableBool:
        ...
    @accumulate.setter
    @abstractmethod
    def accumulate(self, value: NullableBool):
        ...
    @property
    @abstractmethod
    def additive(self) -> BehaviorAdditiveType:
        ...
    @additive.setter
    @abstractmethod
    def additive(self, value: BehaviorAdditiveType):
        ...
    @property
    @abstractmethod
    def properties(self) -> IBehaviorPropertyCollection:
        ...
    @property
    @abstractmethod
    def timing(self) -> ITiming:
        ...
    @timing.setter
    @abstractmethod
    def timing(self, value: ITiming):
        ...