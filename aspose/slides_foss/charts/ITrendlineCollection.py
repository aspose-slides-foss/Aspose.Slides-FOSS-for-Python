from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ITrendline import ITrendline

class ITrendlineCollection(ABC):
    """Represents a collection of TrendlineEx"""
    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        ...

    def add(self, trendline_type) -> ITrendline:
        ...

    def remove(self, value) -> None:
        ...

    def __getitem__(self, index: int) -> ITrendline:
        ...
