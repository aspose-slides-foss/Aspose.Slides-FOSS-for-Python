from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartSeriesReadonly import IChartSeriesReadonly

class IChartSeriesReadonlyCollection(ABC):
    """Represents a readonly collection of"""
    def __getitem__(self, index: int) -> IChartSeriesReadonly:
        ...
