"""
Internal XLSX package support for chart data.

This module provides reading and writing of embedded Excel workbooks
used as data sources for charts in PPTX presentations.
"""

from .xlsx_package import XlsxPackage
from .worksheet_part import WorksheetPart, CellValue
from .workbook_part import WorkbookPart, SheetInfo
from .shared_strings_part import SharedStringsPart
from .table_part import TablePart, TableColumn
from .cell_reference import (
    col_letter_to_index,
    col_index_to_letter,
    parse_cell_ref,
    format_cell_ref,
    parse_range_ref,
    iterate_range,
)

__all__ = [
    'XlsxPackage',
    'WorksheetPart',
    'CellValue',
    'WorkbookPart',
    'SheetInfo',
    'SharedStringsPart',
    'TablePart',
    'TableColumn',
    'col_letter_to_index',
    'col_index_to_letter',
    'parse_cell_ref',
    'format_cell_ref',
    'parse_range_ref',
    'iterate_range',
]
