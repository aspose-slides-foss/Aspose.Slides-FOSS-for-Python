from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartCategory import IChartCategory

class IChartCategoryCollection(ABC):
    """Represents collection of"""
    @property
    def use_cells(self) -> bool:
        """If true then worksheet is used for storing categories (this case supports a multi-level categories). If false then worksheet is NOT used for storing values (and this case doesn't support a multi-level categories). Read/write ."""
        ...

    @use_cells.setter
    def use_cells(self, value: bool):
        ...

    @overload
    def add(self, chart_data_cell) -> IChartCategory:
        ...

    @overload
    def add(self, value) -> IChartCategory:
        ...

    def add(self, *args, **kwargs) -> IChartCategory:
        ...

    def index_of(self, value) -> int:
        ...

    def remove(self, value) -> None:
        ...

    def remove_at(self, index) -> None:
        ...

    def clear(self) -> None:
        ...

    def __getitem__(self, index: int) -> IChartCategory:
        ...
