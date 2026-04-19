from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IPieSplitCustomPoint import IPieSplitCustomPoint

class IPieSplitCustomPointCollection(ABC):
    """Represents a collection of points that shall be drawn in the second pie or bar on a bar-of-pie or pie-of-pie chart with a custom split."""
    def add(self, data_point_index) -> None:
        ...
    def __getitem__(self, index: int) -> IPieSplitCustomPoint:
        ...

