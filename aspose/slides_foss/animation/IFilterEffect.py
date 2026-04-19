from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .FilterEffectRevealType import FilterEffectRevealType
    from .FilterEffectSubtype import FilterEffectSubtype
    from .FilterEffectType import FilterEffectType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class IFilterEffect(IBehavior, ABC):
    """Represent filter effect of behavior."""
    @property
    @abstractmethod
    def reveal(self) -> FilterEffectRevealType:
        """Represents that effect with behavior must reveal (in/out) Read/write ."""
        ...
    @reveal.setter
    @abstractmethod
    def reveal(self, value: FilterEffectRevealType):
        ...
    @property
    @abstractmethod
    def type(self) -> FilterEffectType:
        """Represents type of filter effect. Read/write ."""
        ...
    @type.setter
    @abstractmethod
    def type(self, value: FilterEffectType):
        ...
    @property
    @abstractmethod
    def subtype(self) -> FilterEffectSubtype:
        """Represents subtype of filter effect. Read/write ."""
        ...
    @subtype.setter
    @abstractmethod
    def subtype(self, value: FilterEffectSubtype):
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