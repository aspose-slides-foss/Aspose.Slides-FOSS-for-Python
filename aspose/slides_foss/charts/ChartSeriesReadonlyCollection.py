from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartSeriesReadonlyCollection import IChartSeriesReadonlyCollection

if TYPE_CHECKING:
    from .ChartSeries import ChartSeries


class ChartSeriesReadonlyCollection(IChartSeriesReadonlyCollection):
    """Readonly view of chart series belonging to a single series group."""

    def __len__(self) -> int:
        return len(self._series)

    def __getitem__(self, index: int) -> ChartSeries:
        return self._series[index]

    def __iter__(self):
        return iter(self._series)

    def _init_internal(self, series_list: list):
        self._series: list[ChartSeries] = list(series_list)
