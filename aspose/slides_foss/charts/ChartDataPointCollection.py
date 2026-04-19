from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .IChartDataPoint import IChartDataPoint
    from .IDataSourceTypeForErrorBarsCustomValues import IDataSourceTypeForErrorBarsCustomValues

from .ChartDataPoint import ChartDataPoint
from .ChartDataCell import ChartDataCell
from .DoubleChartValue import DoubleChartValue
from .StringOrDoubleChartValue import StringOrDoubleChartValue
from .DataSourceType import DataSourceType
from .DataSourceTypeForErrorBarsCustomValues import DataSourceTypeForErrorBarsCustomValues
from .IChartDataPointCollection import IChartDataPointCollection


class ChartDataPointCollection(IChartDataPointCollection):
    """Represents collection of data points for a series."""

    def __len__(self) -> int:
        return len(self._points)

    def __getitem__(self, index: int) -> ChartDataPoint:
        return self._points[index]

    def __iter__(self):
        return iter(self._points)

    def _make_double_value(self, value) -> DoubleChartValue:
        """Create a DoubleChartValue from a cell or literal."""
        dv = DoubleChartValue()
        if isinstance(value, ChartDataCell):
            dv._init_internal(DataSourceType.WORKSHEET, cell=value)
        elif isinstance(value, (int, float)):
            dv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=float(value))
        else:
            dv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=float(value) if value is not None else 0.0)
        return dv

    def _make_string_or_double_value(self, value) -> StringOrDoubleChartValue:
        """Create a StringOrDoubleChartValue from a cell or literal."""
        sv = StringOrDoubleChartValue()
        if isinstance(value, ChartDataCell):
            sv._init_internal(DataSourceType.WORKSHEET, cell=value)
        elif isinstance(value, (int, float)):
            sv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=float(value))
        elif isinstance(value, str):
            sv._init_internal(DataSourceType.STRING_LITERALS, literal=value)
        else:
            sv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=float(value) if value is not None else 0.0)
        return sv

    def _add_point(self, **kwargs) -> ChartDataPoint:
        dp = ChartDataPoint()
        dp._init_internal(
            index=len(self._points),
            parent_collection=self,
            **kwargs,
        )
        self._points.append(dp)
        return dp

    # --- Category-based charts (value only) ---

    def add_data_point_for_bar_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_line_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_pie_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_doughnut_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_area_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_radar_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_stock_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    def add_data_point_for_surface_series(self, value) -> IChartDataPoint:
        return self._add_point(value=self._make_double_value(value))

    # --- Scatter (x, y) ---

    def add_data_point_for_scatter_series(self, x_value, y_value) -> IChartDataPoint:
        return self._add_point(
            x_value=self._make_string_or_double_value(x_value),
            y_value=self._make_double_value(y_value),
        )

    # --- Bubble (x, y, size) ---

    def add_data_point_for_bubble_series(self, x_value, y_value, bubble_size) -> IChartDataPoint:
        return self._add_point(
            x_value=self._make_string_or_double_value(x_value),
            y_value=self._make_double_value(y_value),
            bubble_size=self._make_double_value(bubble_size),
        )

    # --- Collection operations ---

    def clear(self) -> None:
        self._points.clear()

    def remove(self, value: ChartDataPoint) -> None:
        self._points.remove(value)
        self._reindex()

    def remove_at(self, index: int) -> None:
        del self._points[index]
        self._reindex()

    def _remove_point(self, point: ChartDataPoint) -> None:
        if point in self._points:
            self._points.remove(point)
            self._reindex()

    def _reindex(self):
        for i, dp in enumerate(self._points):
            dp._index = i

    @property
    def data_source_type_for_error_bars_custom_values(self) -> IDataSourceTypeForErrorBarsCustomValues:
        """Type of values in custom error bars properties. Read-only."""
        return self._ds_type_for_error_bars

    @property
    def data_source_type_for_values(self) -> DataSourceType:
        return self._ds_type_for_values

    @data_source_type_for_values.setter
    def data_source_type_for_values(self, value: DataSourceType):
        self._ds_type_for_values = value

    @property
    def data_source_type_for_x_values(self) -> DataSourceType:
        return self._ds_type_for_x_values

    @data_source_type_for_x_values.setter
    def data_source_type_for_x_values(self, value: DataSourceType):
        self._ds_type_for_x_values = value

    @property
    def data_source_type_for_y_values(self) -> DataSourceType:
        return self._ds_type_for_y_values

    @data_source_type_for_y_values.setter
    def data_source_type_for_y_values(self, value: DataSourceType):
        self._ds_type_for_y_values = value

    @property
    def data_source_type_for_bubble_sizes(self) -> DataSourceType:
        return self._ds_type_for_bubble_sizes

    @data_source_type_for_bubble_sizes.setter
    def data_source_type_for_bubble_sizes(self, value: DataSourceType):
        self._ds_type_for_bubble_sizes = value

    def _init_internal(self, parent_series=None):
        self._points: list[ChartDataPoint] = []
        self._parent_series = parent_series
        self._ds_type_for_error_bars = DataSourceTypeForErrorBarsCustomValues()
        self._ds_type_for_error_bars._init_internal()
        # Default data source types — literals are accepted regardless, but
        # these are exposed as part of the public API.
        self._ds_type_for_values = DataSourceType.DOUBLE_LITERALS
        self._ds_type_for_x_values = DataSourceType.DOUBLE_LITERALS
        self._ds_type_for_y_values = DataSourceType.DOUBLE_LITERALS
        self._ds_type_for_bubble_sizes = DataSourceType.DOUBLE_LITERALS
