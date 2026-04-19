from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IMotionCmdPath import IMotionCmdPath

class IMotionPath(ABC):
    """Represent motion path."""
    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of paths in the collection. Read-only ."""
        ...
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Allows to get base IBehavior interface. Read-only ."""
        ...
    @abstractmethod
    def add(self, type, pts, pts_type, b_relative_coord) -> IMotionCmdPath:
        ...
    @abstractmethod
    def insert(self, index, type, pts, pts_type, b_relative_coord) -> None:
        ...
    @abstractmethod
    def clear(self) -> None:
        ...
    @abstractmethod
    def remove(self, item) -> None:
        ...
    @abstractmethod
    def remove_at(self, index) -> None:
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> IMotionCmdPath:
        ...