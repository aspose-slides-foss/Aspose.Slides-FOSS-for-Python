from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseChartValue import BaseChartValue
from .IStringChartValue import IStringChartValue

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType
    from .ChartDataCell import ChartDataCell


class StringChartValue(IStringChartValue, BaseChartValue):
    """Represents a string value backed by workbook cells or literal."""

    @property
    def as_literal_string(self) -> str:
        if self._cells:
            return str(self._cells[0].value or '')
        return str(self._data) if self._data is not None else ''

    @as_literal_string.setter
    def as_literal_string(self, value: str):
        from .DataSourceType import DataSourceType
        if self._cells:
            self._cells[0].value = value
        else:
            self._data = value
            self._data_source_type = DataSourceType.STRING_LITERALS

    def set_from_one_cell(self, cell: 'ChartDataCell') -> None:
        from .DataSourceType import DataSourceType
        self._cells = [cell]
        self._data_source_type = DataSourceType.WORKSHEET
        self._data = cell

    def to_string(self) -> str:
        return self.as_literal_string

    def _init_internal(self, data_source_type: 'DataSourceType',
                       cells: list = None, literal: str = None):
        super()._init_internal(data_source_type, cells[0] if cells else literal)
        self._cells = cells or []
