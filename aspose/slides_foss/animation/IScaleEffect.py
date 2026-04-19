from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class IScaleEffect(IBehavior, ABC):
    """Represents animation scale effect."""
    @property
    @abstractmethod
    def zoom_content(self) -> NullableBool:
        """Determines whether a content should be zoomed. Read/write ."""
        ...
    @zoom_content.setter
    @abstractmethod
    def zoom_content(self, value: NullableBool):
        ...
    @property
    @abstractmethod
    def from_address(self) -> Any:
        """Specifies an x/y co-ordinate to start the animation from (in percents). Read/write ."""
        ...
    @from_address.setter
    @abstractmethod
    def from_address(self, value: Any):
        ...
    @property
    @abstractmethod
    def to(self) -> Any:
        """Specifies the target location for an animation scale effect (in percents). Read/write ."""
        ...
    @to.setter
    @abstractmethod
    def to(self, value: Any):
        ...
    @property
    @abstractmethod
    def by(self) -> Any:
        """describes the relative offset value for the animation (in percents). Read/write ."""
        ...
    @by.setter
    @abstractmethod
    def by(self, value: Any):
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