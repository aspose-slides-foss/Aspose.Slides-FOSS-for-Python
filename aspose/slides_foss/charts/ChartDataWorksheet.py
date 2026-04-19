from __future__ import annotations
from .IChartDataWorksheet import IChartDataWorksheet


class ChartDataWorksheet(IChartDataWorksheet):
    """Represents a worksheet in the chart data workbook."""

    @property
    def name(self) -> str:
        return self._name

    @property
    def index(self) -> int:
        return self._index

    def _init_internal(self, name: str, index: int):
        self._name = name
        self._index = index
