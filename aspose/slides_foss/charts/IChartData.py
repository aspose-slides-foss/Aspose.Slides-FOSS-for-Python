from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ChartDataSourceType import ChartDataSourceType
    from .IChartCategoryCollection import IChartCategoryCollection
    from .IChartDataWorkbook import IChartDataWorkbook
    from .IChartSeriesCollection import IChartSeriesCollection
    from .IChartSeriesGroupCollection import IChartSeriesGroupCollection

class IChartData(ABC):
    """Represents data used for a chart plotting."""
    @property
    def chart_data_workbook(self) -> IChartDataWorkbook:
        """Gets the cells factory to create cells used for chart series or categories. Read-only ."""
        ...

    @property
    def series(self) -> IChartSeriesCollection:
        """Gets the series. Read-only ."""
        ...

    @property
    def series_groups(self) -> IChartSeriesGroupCollection:
        """Gets the groups of series. Read-only ."""
        ...

    @property
    def categories(self) -> IChartCategoryCollection:
        """Gets the primary categories (or both primary and secondary categories if property is false). Read-only ."""
        ...

    @property
    def data_source_type(self) -> ChartDataSourceType:
        """Represents data source of the chart"""
        ...

    def set_range(self, formula) -> None:
        ...

    def get_range(self) -> str:
        ...
