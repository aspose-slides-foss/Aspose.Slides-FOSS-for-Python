from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IBehavior import IBehavior

class IBehaviorCollection(ABC):
    """Represents collection of behavior effects."""
    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of behaviors in a collection. Read-only ."""
        ...
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interface. Read-only ."""
        ...
    @abstractmethod
    def add(self, item) -> None:
        ...
    @abstractmethod
    def index_of(self, item) -> int:
        ...
    @abstractmethod
    def insert(self, index, item) -> None:
        ...
    @abstractmethod
    def remove(self, item) -> bool:
        ...
    @abstractmethod
    def remove_at(self, index) -> None:
        ...
    @abstractmethod
    def clear(self) -> None:
        ...
    @abstractmethod
    def contains(self, item) -> bool:
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> IBehavior:
        ...