from __future__ import annotations
from typing import TYPE_CHECKING

from .ChartDataPointCollection import ChartDataPointCollection
from .TrendlineCollection import TrendlineCollection
from .IChartSeries import IChartSeries

if TYPE_CHECKING:
    from .ChartSeriesGroup import ChartSeriesGroup
    from .ChartType import ChartType
    from .StringChartValue import StringChartValue
    from .ErrorBarsFormat import ErrorBarsFormat
    from .DataLabelCollection import DataLabelCollection
    from .Marker import Marker
    from .IChartDataPointCollection import IChartDataPointCollection
    from .IChartSeriesGroup import IChartSeriesGroup
    from .IDataLabelCollection import IDataLabelCollection
    from .IErrorBarsFormat import IErrorBarsFormat
    from .IMarker import IMarker
    from .IStringChartValue import IStringChartValue
    from .ITrendlineCollection import ITrendlineCollection


class ChartSeries(IChartSeries):
    """Represents a chart series."""

    @property
    def name(self) -> IStringChartValue:
        return self._name

    @property
    def data_points(self) -> IChartDataPointCollection:
        return self._data_points

    @property
    def type(self) -> ChartType:
        return self._type

    @type.setter
    def type(self, value: ChartType):
        self._type = value

    @property
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, value: int):
        self._order = value

    @property
    def parent_series_group(self) -> IChartSeriesGroup:
        if self._chart_data is not None:
            if self._parent_series_group is None or self._chart_data._series_groups_dirty:
                # Trigger lazy rebuild of series groups which sets the back-link
                _ = self._chart_data.series_groups
        return self._parent_series_group

    @property
    def overlap(self) -> int:
        return self.parent_series_group.overlap

    @property
    def gap_width(self) -> int:
        return self.parent_series_group.gap_width

    @property
    def gap_depth(self) -> int:
        return self.parent_series_group.gap_depth

    @property
    def first_slice_angle(self) -> int:
        return self.parent_series_group.first_slice_angle

    @property
    def doughnut_hole_size(self) -> int:
        return self.parent_series_group.doughnut_hole_size

    @property
    def is_color_varied(self) -> bool:
        return self.parent_series_group.is_color_varied

    @property
    def has_series_lines(self) -> bool:
        return self.parent_series_group.has_series_lines

    @property
    def second_pie_size(self) -> int:
        return self.parent_series_group.second_pie_size

    @property
    def bubble_size_scale(self) -> int:
        return self.parent_series_group.bubble_size_scale

    @property
    def bubble_size_representation(self):
        return self.parent_series_group.bubble_size_representation

    @property
    def pie_split_position(self) -> float:
        return self.parent_series_group.pie_split_position

    @property
    def pie_split_by(self):
        return self.parent_series_group.pie_split_by

    @property
    def plot_on_second_axis(self) -> bool:
        grp = self.parent_series_group
        if grp is not None:
            return grp.plot_on_second_axis
        return False

    @plot_on_second_axis.setter
    def plot_on_second_axis(self, value: bool):
        if self.plot_on_second_axis == value:
            return
        if self._chart_data is None:
            return
        self._chart_data._move_series_to_axis(self, value)

    @property
    def trend_lines(self) -> ITrendlineCollection:
        return self._trend_lines

    @property
    def error_bars_x_format(self) -> IErrorBarsFormat | None:
        """ErrorBars with X direction. Available for scatter and bubble series."""
        return self._error_bars_x

    @property
    def error_bars_y_format(self) -> IErrorBarsFormat | None:
        """ErrorBars with Y direction. Available for area, bar, line, scatter, bubble series."""
        return self._error_bars_y

    @property
    def marker(self) -> 'IMarker':
        """Series marker (applies to all data points unless overridden). Read-only."""
        from .Marker import Marker
        chart_part = getattr(self._chart_data, '_chart_part', None) if self._chart_data else None
        m = Marker()
        m._init_internal(self, chart_part, point_index=None)
        return m

    @property
    def labels(self) -> IDataLabelCollection:
        """Returns the data labels of this series. Read-only."""
        if self._data_labels is None:
            from .DataLabelCollection import DataLabelCollection
            chart_part = None
            if self._chart_data is not None:
                chart_part = getattr(self._chart_data, '_chart_part', None)
            dlc = DataLabelCollection()
            dlc._init_internal(parent_series=self, chart_part=chart_part)
            self._data_labels = dlc
        return self._data_labels

    def _init_internal(self, name: 'StringChartValue', chart_type: 'ChartType',
                       order: int = 0):
        self._name = name
        self._type = chart_type
        self._order = order
        self._parent_series_group = None
        self._chart_data = None  # set by ChartSeriesCollection
        self._data_points = ChartDataPointCollection()
        self._data_points._init_internal(parent_series=self)
        self._trend_lines = TrendlineCollection()
        self._trend_lines._init_internal(chart_part=None)
        self._error_bars_x = None
        self._error_bars_y = None
        self._init_error_bars_for_type(chart_type)
        # Data labels state: <c:dLbls> element preserved across save rebuilds.
        self._dlbls_elem = None
        self._data_labels = None
        # Marker state preserved across save rebuilds:
        #   _marker_elem — series-level <c:marker>
        #   _dpt_elems   — per-point {index: <c:dPt>} (dPt may carry marker,
        #                  invertIfNegative, spPr, bubble3D, etc.)
        self._marker_elem = None
        self._dpt_elems: dict[int, object] = {}
        # Per-point "value from cell" mapping: {point_index: ChartDataCell}.
        # Emitted as a single <c15:datalabelsRange> at the <c:ser>/extLst level.
        self._value_from_cell_cells = None

    def _init_error_bars_for_type(self, chart_type):
        """Create error bar format objects based on chart type capabilities."""
        from .ErrorBarsFormat import ErrorBarsFormat
        ct = chart_type.value if hasattr(chart_type, 'value') else str(chart_type)
        has_x, has_y = _error_bar_support(ct)
        if has_x:
            self._error_bars_x = ErrorBarsFormat()
            self._error_bars_x._init_internal('x')
        if has_y:
            self._error_bars_y = ErrorBarsFormat()
            self._error_bars_y._init_internal('y')


# Chart types that support X error bars (scatter/bubble families)
_X_ERROR_BAR_TYPES = frozenset({
    'ScatterWithMarkers', 'ScatterWithSmoothLines', 'ScatterWithSmoothLinesAndMarkers',
    'ScatterWithStraightLines', 'ScatterWithStraightLinesAndMarkers',
    'Bubble', 'BubbleWith3DEffect',
})

# Chart types that support Y error bars (most category-based + scatter/bubble)
_NO_Y_ERROR_BAR_TYPES = frozenset({
    'Pie', 'ExplodedPie', 'Pie3D', 'ExplodedPie3D', 'PieOfPie', 'BarOfPie',
    'Doughnut', 'ExplodedDoughnut',
})


def _error_bar_support(chart_type_value: str) -> tuple[bool, bool]:
    """Return (has_x, has_y) for a given chart type value string."""
    has_x = chart_type_value in _X_ERROR_BAR_TYPES
    has_y = chart_type_value not in _NO_Y_ERROR_BAR_TYPES
    return has_x, has_y
