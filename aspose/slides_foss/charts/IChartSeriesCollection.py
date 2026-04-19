from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartSeries import IChartSeries

class IChartSeriesCollection(ABC):
    """Represents collection of"""
    @overload
    def add(self, type) -> IChartSeries:
        ...

    @overload
    def add(self, cell_with_series_name, type) -> IChartSeries:
        ...

    @overload
    def add(self, cells_with_series_name, type) -> IChartSeries:
        ...

    @overload
    def add(self, name, type) -> IChartSeries:
        ...

    def add(self, *args, **kwargs) -> IChartSeries:
        ...

    def insert(self, index, type) -> IChartSeries:
        ...

    def index_of(self, value) -> int:
        ...

    def remove(self, value) -> None:
        ...

    def remove_at(self, index) -> None:
        ...

    def clear(self) -> None:
        ...

    def __getitem__(self, index: int) -> IChartSeries:
        ...
