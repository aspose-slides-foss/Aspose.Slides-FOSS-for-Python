from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ISequence import ISequence

class ISequenceCollection(ABC):
    """Represents collection of interactive sequences."""
    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of elements in a collection Read-only ."""
        ...
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interface. Read-only ."""
        ...
    @abstractmethod
    def add(self, shape_trigger) -> ISequence:
        ...
    @abstractmethod
    def remove(self, item) -> None:
        ...
    @abstractmethod
    def remove_at(self, index) -> None:
        ...
    @abstractmethod
    def clear(self) -> None:
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> ISequence:
        ...