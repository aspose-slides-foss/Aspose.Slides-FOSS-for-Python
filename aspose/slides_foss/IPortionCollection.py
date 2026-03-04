from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IPortion import IPortion

class IPortionCollection(ABC):
    """Represents a collection of a portions."""
    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        ...

    @property
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interface. Read-only ."""
        ...
    def add(self, value) -> None:
        ...
    def index_of(self, item) -> int:
        ...
    def insert(self, index, value) -> None:
        ...
    def clear(self) -> None:
        ...
    def contains(self, item) -> bool:
        ...
    def remove(self, item) -> bool:
        ...
    def remove_at(self, index) -> None:
        ...
    def __getitem__(self, index: int) -> IPortion:
        ...
