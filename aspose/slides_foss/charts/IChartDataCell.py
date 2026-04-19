from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IChartDataWorksheet import IChartDataWorksheet

class IChartDataCell(ABC):
    """Represents cell for chart data."""
    @property
    def row(self) -> int:
        """Returns the index of the row of worksheet in which the cell is located. Read-only ."""
        ...

    @property
    def column(self) -> int:
        """Returns the index of the column of worksheet in which the cell is located. Read-only ."""
        ...

    @property
    def value(self) -> object:
        """Gets or sets the value of a cell. Read/write ."""
        ...

    @value.setter
    def value(self, value: object):
        ...

    @property
    def chart_data_worksheet(self) -> IChartDataWorksheet:
        """Gets the worksheet. Read-only ."""
        ...
