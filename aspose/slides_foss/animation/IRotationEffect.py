from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class IRotationEffect(IBehavior, ABC):
    """Represent rotation behavior of effect."""
    @property
    @abstractmethod
    def from_address(self) -> float:
        """Describes the starting value for the animation. Read/write ."""
        ...
    @from_address.setter
    @abstractmethod
    def from_address(self, value: float):
        ...
    @property
    @abstractmethod
    def to(self) -> float:
        """Describes the ending value for the animation. Read/write ."""
        ...
    @to.setter
    @abstractmethod
    def to(self, value: float):
        ...
    @property
    @abstractmethod
    def by(self) -> float:
        """Describes the relative offset value for the animation. Read/write ."""
        ...
    @by.setter
    @abstractmethod
    def by(self, value: float):
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