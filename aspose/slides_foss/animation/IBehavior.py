from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class IBehavior(ABC):
    """Represent base class behavior of effect."""
    @property
    @abstractmethod
    def accumulate(self) -> NullableBool:
        """Represents whether animation behaviors are accumulated. Read/write ."""
        ...
    @accumulate.setter
    @abstractmethod
    def accumulate(self, value: NullableBool):
        ...
    @property
    @abstractmethod
    def additive(self) -> BehaviorAdditiveType:
        """Represents whether the current animation behavior is combined with other running animations. Read/write ."""
        ...
    @additive.setter
    @abstractmethod
    def additive(self, value: BehaviorAdditiveType):
        ...
    @property
    @abstractmethod
    def properties(self) -> IBehaviorPropertyCollection:
        """Represents properties of behavior. Read-only ."""
        ...
    @property
    @abstractmethod
    def timing(self) -> ITiming:
        """Represents timing properties for the effect behavior. Read/write ."""
        ...
    @timing.setter
    @abstractmethod
    def timing(self, value: ITiming):
        ...