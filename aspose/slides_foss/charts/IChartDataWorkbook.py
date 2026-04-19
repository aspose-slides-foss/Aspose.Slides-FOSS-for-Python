from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from .IChartCellCollection import IChartCellCollection
    from .IChartDataCell import IChartDataCell
    from .IChartDataWorksheetCollection import IChartDataWorksheetCollection

class IChartDataWorkbook(ABC):
    """Provides access to embedded Excel workbook"""
    @property
    def worksheets(self) -> IChartDataWorksheetCollection:
        """Gets a collection of worksheets."""
        ...

    @overload
    def get_cell(self, worksheet_name, row, column) -> IChartDataCell:
        ...

    @overload
    def get_cell(self, worksheet_index, row, column) -> IChartDataCell:
        ...

    @overload
    def get_cell(self, worksheet_index, cell_name) -> IChartDataCell:
        ...

    @overload
    def get_cell(self, worksheet_index, cell_name, value) -> IChartDataCell:
        ...

    @overload
    def get_cell(self, worksheet_index, row, column, value) -> IChartDataCell:
        ...

    def get_cell(self, *args, **kwargs) -> IChartDataCell:
        ...

    def clear(self, sheet_index) -> None:
        ...
