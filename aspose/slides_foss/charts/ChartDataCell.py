from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartDataCell import IChartDataCell

if TYPE_CHECKING:
    from .ChartDataWorkbook import ChartDataWorkbook
    from .ChartDataWorksheet import ChartDataWorksheet
    from .IChartDataWorksheet import IChartDataWorksheet


class ChartDataCell(IChartDataCell):
    """Represents a cell in the chart data workbook."""

    @property
    def row(self) -> int:
        """0-based row index."""
        return self._row

    @property
    def column(self) -> int:
        """0-based column index."""
        return self._column

    @property
    def value(self) -> object:
        """Gets or sets the cell value."""
        return self._workbook._read_cell(self._worksheet_index, self._row, self._column)

    @value.setter
    def value(self, value: object):
        self._workbook._write_cell(self._worksheet_index, self._row, self._column, value)

    @property
    def chart_data_worksheet(self) -> IChartDataWorksheet:
        return self._workbook._get_worksheet(self._worksheet_index)

    def _init_internal(self, workbook: 'ChartDataWorkbook', worksheet_index: int,
                       row: int, column: int):
        self._workbook = workbook
        self._worksheet_index = worksheet_index
        self._row = row
        self._column = column
