from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseChartValue import BaseChartValue
from .IDoubleChartValue import IDoubleChartValue

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType
    from .ChartDataCell import ChartDataCell
    from .IChartDataCell import IChartDataCell


class DoubleChartValue(IDoubleChartValue, BaseChartValue):
    """Represents a double value backed by a workbook cell or literal."""

    @property
    def as_cell(self) -> IChartDataCell:
        return self._cell

    @as_cell.setter
    def as_cell(self, value: ChartDataCell):
        from .DataSourceType import DataSourceType
        self._cell = value
        self._data_source_type = DataSourceType.WORKSHEET
        self._data = value

    @property
    def as_literal_double(self) -> float:
        if self._cell is not None:
            val = self._cell.value
            return float(val) if val is not None else 0.0
        return float(self._data) if self._data is not None else 0.0

    @as_literal_double.setter
    def as_literal_double(self, value: float):
        from .DataSourceType import DataSourceType
        if self._cell is not None:
            self._cell.value = value
        else:
            self._data = value
            self._data_source_type = DataSourceType.DOUBLE_LITERALS

    def to_double(self) -> float:
        return self.as_literal_double

    def _init_internal(self, data_source_type: 'DataSourceType',
                       cell: 'ChartDataCell' = None, literal: float = None):
        super()._init_internal(data_source_type, cell if cell else literal)
        self._cell = cell
