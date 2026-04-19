from __future__ import annotations
from typing import TYPE_CHECKING, Union

from .ChartSeries import ChartSeries
from .StringChartValue import StringChartValue
from .DataSourceType import DataSourceType
from .IChartSeriesCollection import IChartSeriesCollection

if TYPE_CHECKING:
    from .ChartType import ChartType
    from .ChartDataCell import ChartDataCell
    from .ChartData import ChartData
    from .IChartSeries import IChartSeries


class ChartSeriesCollection(IChartSeriesCollection):
    """Represents collection of chart series."""

    def __len__(self) -> int:
        return len(self._series)

    def __getitem__(self, index: int) -> ChartSeries:
        return self._series[index]

    def __iter__(self):
        return iter(self._series)

    def add(self, *args, **kwargs) -> IChartSeries:
        """
        Add a series. Overloads:
        - add(type) — empty series with default name
        - add(name: str, type) — series with literal name
        - add(cell: ChartDataCell, type) — series with cell-backed name
        """
        from .ChartType import ChartType

        if len(args) == 1 and isinstance(args[0], ChartType):
            chart_type = args[0]
            name_val = StringChartValue()
            name_val._init_internal(DataSourceType.STRING_LITERALS, literal=f'Series {len(self._series) + 1}')
            return self._add_series(name_val, chart_type)

        if len(args) == 2:
            name_or_cell, chart_type = args[0], args[1]
            if isinstance(name_or_cell, str):
                name_val = StringChartValue()
                name_val._init_internal(DataSourceType.STRING_LITERALS, literal=name_or_cell)
            elif hasattr(name_or_cell, 'row'):
                # ChartDataCell
                name_val = StringChartValue()
                name_val._init_internal(DataSourceType.WORKSHEET, cells=[name_or_cell])
            else:
                name_val = StringChartValue()
                name_val._init_internal(DataSourceType.STRING_LITERALS, literal=str(name_or_cell))
            return self._add_series(name_val, chart_type)

        raise TypeError(f"Invalid arguments to add: {args}")

    def _add_series(self, name: StringChartValue, chart_type: 'ChartType') -> ChartSeries:
        series = ChartSeries()
        series._init_internal(name=name, chart_type=chart_type, order=len(self._series))
        series._chart_data = self._chart_data
        self._series.append(series)
        self._invalidate_groups()
        return series

    def insert(self, index: int, chart_type: 'ChartType') -> IChartSeries:
        name_val = StringChartValue()
        name_val._init_internal(DataSourceType.STRING_LITERALS, literal=f'Series {len(self._series) + 1}')
        series = ChartSeries()
        series._init_internal(name=name_val, chart_type=chart_type, order=index)
        series._chart_data = self._chart_data
        self._series.insert(index, series)
        self._reindex()
        self._invalidate_groups()
        return series

    def index_of(self, value: ChartSeries) -> int:
        return self._series.index(value)

    def remove(self, value: ChartSeries) -> None:
        self._series.remove(value)
        self._reindex()
        self._invalidate_groups()

    def remove_at(self, index: int) -> None:
        del self._series[index]
        self._reindex()
        self._invalidate_groups()

    def clear(self) -> None:
        self._series.clear()
        self._invalidate_groups()

    def _reindex(self):
        for i, s in enumerate(self._series):
            s._order = i

    def _invalidate_groups(self):
        if self._chart_data is not None:
            self._chart_data._invalidate_series_groups()

    def _init_internal(self, chart_data: 'ChartData' = None):
        self._series: list[ChartSeries] = []
        self._chart_data = chart_data
