from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartCell import IChartCell

class IChartCellCollection(ABC):
    """Represents collection of a cells with data."""
    @property
    def count(self) -> int:
        """Gets the count of cells in collection. Read-only ."""
        ...


    @overload
    def add(self, chart_data_cell) -> None:
        ...

    @overload
    def add(self, value) -> None:
        ...

    def add(self, *args, **kwargs) -> None:
        ...
    def remove_at(self, index) -> None:
        ...
    def __getitem__(self, index: int) -> IChartCell:
        ...

