from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartSeriesGroup import IChartSeriesGroup

class IChartSeriesGroupCollection(ABC):
    """Represents the collection of groups of combinable series."""
    def __getitem__(self, index: int) -> IChartSeriesGroup:
        ...
