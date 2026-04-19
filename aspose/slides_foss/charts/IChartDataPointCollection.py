from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType
    from .IChartDataPoint import IChartDataPoint
    from .IDataSourceTypeForErrorBarsCustomValues import IDataSourceTypeForErrorBarsCustomValues

class IChartDataPointCollection(ABC):
    """Represents collection of a series data point."""
    @property
    def data_source_type_for_x_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points XValue property object. In other words it specifies the type of value of ChartDataPointEx.XValue.Data property. Read/write ."""
        ...

    @data_source_type_for_x_values.setter
    def data_source_type_for_x_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_y_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points YValue property object. In other words it specifies the type of value of ChartDataPointEx.YValue.Data property. Read/write ."""
        ...

    @data_source_type_for_y_values.setter
    def data_source_type_for_y_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_bubble_sizes(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points BubbleSize property object. In other words it specifies the type of value of ChartDataPointEx.BubbleSize.Data property. Read/write ."""
        ...

    @data_source_type_for_bubble_sizes.setter
    def data_source_type_for_bubble_sizes(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points Value property object. In other words it specifies the type of value of ChartDataPoint.Value.Data property. Read/write ."""
        ...

    @data_source_type_for_values.setter
    def data_source_type_for_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_error_bars_custom_values(self) -> IDataSourceTypeForErrorBarsCustomValues:
        """Specifies the type of values in ChartDataPoint.ErrorBarsCustomValues properties list. Read-only ."""
        ...

    @overload
    def add_data_point_for_stock_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_stock_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_stock_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_line_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_line_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_line_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        ...

    def add_data_point_for_scatter_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_radar_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_radar_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_radar_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bar_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bar_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_bar_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_area_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_area_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_area_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_pie_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_pie_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_pie_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_doughnut_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_doughnut_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_doughnut_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        ...

    def add_data_point_for_bubble_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_surface_series(self, value) -> IChartDataPoint:
        ...

    @overload
    def add_data_point_for_surface_series(self, value) -> IChartDataPoint:
        ...

    def add_data_point_for_surface_series(self, *args, **kwargs) -> IChartDataPoint:
        ...

    def clear(self) -> None:
        ...

    def remove(self, value) -> None:
        ...

    def remove_at(self, index) -> None:
        ...

    def __getitem__(self, index: int) -> IChartDataPoint:
        ...
