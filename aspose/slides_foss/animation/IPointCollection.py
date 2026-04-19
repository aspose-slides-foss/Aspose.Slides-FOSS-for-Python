from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IPoint import IPoint

class IPointCollection(ABC):
    """Represents a collection of portions."""
    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of points in the collection. Read-only ."""
        ...
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Allows to get base IEnumerable interface. Read-only ."""
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> IPoint:
        ...