from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartDataPoint import IChartDataPoint

if TYPE_CHECKING:
    from .DoubleChartValue import DoubleChartValue
    from .StringOrDoubleChartValue import StringOrDoubleChartValue
    from .ErrorBarsCustomValues import ErrorBarsCustomValues
    from .DataLabel import DataLabel
    from .Marker import Marker
    from .IDataLabel import IDataLabel
    from .IDoubleChartValue import IDoubleChartValue
    from .IErrorBarsCustomValues import IErrorBarsCustomValues
    from .IMarker import IMarker
    from .IStringOrDoubleChartValue import IStringOrDoubleChartValue


class ChartDataPoint(IChartDataPoint):
    """Represents a series data point."""

    @property
    def index(self) -> int:
        return self._index

    @property
    def value(self) -> IDoubleChartValue:
        """Value for category-based charts (bar, line, pie, area, etc.)."""
        return self._value

    @property
    def x_value(self) -> IStringOrDoubleChartValue:
        """X value for scatter/bubble charts."""
        return self._x_value

    @property
    def y_value(self) -> IDoubleChartValue:
        """Y value for scatter/bubble charts."""
        return self._y_value

    @property
    def bubble_size(self) -> IDoubleChartValue:
        """Bubble size for bubble charts."""
        return self._bubble_size

    @property
    def error_bars_custom_values(self) -> IErrorBarsCustomValues:
        """Custom error bar values for this data point. Read-only."""
        if self._error_bars_custom_values is None:
            from .ErrorBarsCustomValues import ErrorBarsCustomValues
            self._error_bars_custom_values = ErrorBarsCustomValues()
            self._error_bars_custom_values._init_internal()
        return self._error_bars_custom_values

    @property
    def marker(self) -> 'IMarker':
        """Marker for this specific data point (overrides series marker). Read-only."""
        from .Marker import Marker
        series = self._parent_collection._parent_series if self._parent_collection else None
        if series is None:
            return None
        chart_part = getattr(series._chart_data, '_chart_part', None) if series._chart_data else None
        m = Marker()
        m._init_internal(series, chart_part, point_index=self._index)
        return m

    @property
    def label(self) -> IDataLabel:
        """Data label for this data point. Read-only."""
        series = self._parent_collection._parent_series if self._parent_collection else None
        if series is None:
            return None
        return series.labels[self._index]

    def remove(self) -> None:
        """Remove this data point from its collection."""
        if self._parent_collection is not None:
            self._parent_collection._remove_point(self)

    def _init_internal(self, index: int, value=None, x_value=None,
                       y_value=None, bubble_size=None,
                       parent_collection=None):
        self._index = index
        self._value = value
        self._x_value = x_value
        self._y_value = y_value
        self._bubble_size = bubble_size
        self._parent_collection = parent_collection
        self._error_bars_custom_values = None
