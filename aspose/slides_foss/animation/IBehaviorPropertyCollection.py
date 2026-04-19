from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IBehaviorProperty import IBehaviorProperty

class IBehaviorPropertyCollection(ABC):
    """Represents timing properties for the effect behavior."""
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interfaces. Read-only ."""
        ...
    @abstractmethod
    def add(self, property_value) -> None:
        ...
    @abstractmethod
    def index_of(self, property_value) -> int:
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> IBehaviorProperty:
        ...