from __future__ import annotations
from typing import TYPE_CHECKING, Union

from .ChartDataCell import ChartDataCell
from .ChartDataWorksheet import ChartDataWorksheet
from .IChartDataWorkbook import IChartDataWorkbook

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .._internal.xlsx.xlsx_package import XlsxPackage
    from .._internal.xlsx.cell_reference import format_cell_ref
    from .IChartDataCell import IChartDataCell
    from .IChartDataWorksheetCollection import IChartDataWorksheetCollection


class ChartDataWorkbook(IChartDataWorkbook):
    """Provides access to the embedded Excel workbook for chart data."""

    @property
    def worksheets(self) -> list[IChartDataWorksheetCollection]:
        """Gets all worksheets."""
        xlsx = self._chart_part.get_xlsx()
        result = []
        for i, name in enumerate(xlsx.get_sheet_names()):
            ws = ChartDataWorksheet()
            ws._init_internal(name, i)
            result.append(ws)
        return result

    def get_cell(self, *args, **kwargs) -> IChartDataCell:
        """
        Get a cell from the workbook. Overloads:
        - get_cell(worksheet_index, row, column)
        - get_cell(worksheet_index, row, column, value)
        - get_cell(worksheet_index, cell_name)
        - get_cell(worksheet_index, cell_name, value)
        - get_cell(worksheet_name, row, column)
        """
        if len(args) >= 3 and isinstance(args[0], str) and isinstance(args[1], int):
            # get_cell(worksheet_name, row, column)
            ws_name = args[0]
            row, col = args[1], args[2]
            ws_idx = self._resolve_ws_index(ws_name)
            cell = self._make_cell(ws_idx, row, col)
            if len(args) >= 4:
                cell.value = args[3]
            return cell

        if len(args) >= 2 and isinstance(args[0], int) and isinstance(args[1], str):
            # get_cell(worksheet_index, cell_name) or get_cell(worksheet_index, cell_name, value)
            from .._internal.xlsx.cell_reference import parse_cell_ref
            ws_idx = args[0]
            row, col = parse_cell_ref(args[1])
            cell = self._make_cell(ws_idx, row, col)
            if len(args) >= 3:
                cell.value = args[2]
            return cell

        if len(args) >= 3 and isinstance(args[0], int) and isinstance(args[1], int):
            # get_cell(worksheet_index, row, column) or get_cell(worksheet_index, row, column, value)
            ws_idx, row, col = args[0], args[1], args[2]
            cell = self._make_cell(ws_idx, row, col)
            if len(args) >= 4:
                cell.value = args[3]
            return cell

        raise TypeError(f"Invalid arguments to get_cell: {args}")

    def clear(self, sheet_index: int) -> None:
        """Clear all data from a worksheet."""
        xlsx = self._chart_part.get_xlsx()
        ws = xlsx.get_worksheet(sheet_index)
        if ws:
            # Clear by creating fresh empty worksheet
            ws._create_empty()
        self._chart_part.mark_xlsx_dirty()

    def _init_internal(self, chart_part: 'ChartPart'):
        self._chart_part = chart_part

    def _resolve_ws_index(self, name: str) -> int:
        xlsx = self._chart_part.get_xlsx()
        for i, ws_name in enumerate(xlsx.get_sheet_names()):
            if ws_name == name:
                return i
        raise ValueError(f"Worksheet not found: {name}")

    def _make_cell(self, worksheet_index: int, row: int, column: int) -> ChartDataCell:
        cell = ChartDataCell()
        cell._init_internal(self, worksheet_index, row, column)
        return cell

    def _get_worksheet(self, index: int) -> ChartDataWorksheet:
        xlsx = self._chart_part.get_xlsx()
        names = xlsx.get_sheet_names()
        ws = ChartDataWorksheet()
        ws._init_internal(names[index] if index < len(names) else f'Sheet{index+1}', index)
        return ws

    def _read_cell(self, worksheet_index: int, row: int, column: int):
        """Read a cell value from the embedded XLSX."""
        from .._internal.xlsx.cell_reference import format_cell_ref
        xlsx = self._chart_part.get_xlsx()
        ws = xlsx.get_worksheet(worksheet_index)
        if ws is None:
            return None
        ref = format_cell_ref(row, column)
        cell_val = ws.get_cell(ref)
        return cell_val.value

    def _write_cell(self, worksheet_index: int, row: int, column: int, value):
        """Write a cell value to the embedded XLSX."""
        from .._internal.xlsx.cell_reference import format_cell_ref
        xlsx = self._chart_part.get_xlsx()
        ws = xlsx.get_worksheet(worksheet_index)
        if ws is None:
            return
        ref = format_cell_ref(row, column)
        ws.set_cell(ref, value)
        self._chart_part.mark_xlsx_dirty()
