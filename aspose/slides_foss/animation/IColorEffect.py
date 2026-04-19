from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .ColorDirection import ColorDirection
    from .ColorSpace import ColorSpace
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from ..IColorFormat import IColorFormat
    from .IColorOffset import IColorOffset
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class IColorEffect(IBehavior, ABC):
    """Represents a color effect for an animation behavior."""
    @property
    @abstractmethod
    def from_address(self) -> IColorFormat:
        """This value is used to specify the starting color of behavior. Read/write ."""
        ...
    @from_address.setter
    @abstractmethod
    def from_address(self, value: IColorFormat):
        ...
    @property
    @abstractmethod
    def to(self) -> IColorFormat:
        """Describes resulting color for the animation color change. Read/write ."""
        ...
    @to.setter
    @abstractmethod
    def to(self, value: IColorFormat):
        ...
    @property
    @abstractmethod
    def by(self) -> IColorOffset:
        """Describes the relative offset value for the color animation. Read/write ."""
        ...
    @by.setter
    @abstractmethod
    def by(self, value: IColorOffset):
        ...
    @property
    @abstractmethod
    def color_space(self) -> ColorSpace:
        """Represent color space of behavior. Read/write ."""
        ...
    @color_space.setter
    @abstractmethod
    def color_space(self, value: ColorSpace):
        ...
    @property
    @abstractmethod
    def direction(self) -> ColorDirection:
        """Specifies which direction to cycle the hue around the color wheel. Read/write ."""
        ...
    @direction.setter
    @abstractmethod
    def direction(self, value: ColorDirection):
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