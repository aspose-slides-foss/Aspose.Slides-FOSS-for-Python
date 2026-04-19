from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .BubbleSizeRepresentationType import BubbleSizeRepresentationType
    from .ChartShapeType import ChartShapeType
    from .ChartType import ChartType
    from ..drawing import Color
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartDataPointCollection import IChartDataPointCollection
    from .IChartSeriesGroup import IChartSeriesGroup
    from ..IColorFormat import IColorFormat
    from .IDataLabelCollection import IDataLabelCollection
    from .IErrorBarsFormat import IErrorBarsFormat
    from .IFormat import IFormat
    from .ILegendEntryProperties import ILegendEntryProperties
    from .IMarker import IMarker
    from .IPieSplitCustomPointCollection import IPieSplitCustomPointCollection
    from ..IPresentation import IPresentation
    from .IStringChartValue import IStringChartValue
    from .ITrendlineCollection import ITrendlineCollection
    from .PieSplitType import PieSplitType

class IChartSeries(IChartComponent, ABC):
    """Represents a chart series."""
    @property
    def marker(self) -> IMarker:
        """Return series marker. Read-only ."""
        ...

    @property
    def name(self) -> IStringChartValue:
        """Return series name. Read-only ."""
        ...

    @property
    def data_points(self) -> IChartDataPointCollection:
        """Returns collection of data points of this series. Read-only ."""
        ...

    @property
    def type(self) -> ChartType:
        """Returns a type of this series. Read/write ."""
        ...

    @type.setter
    def type(self, value: ChartType):
        ...

    @property
    def parent_series_group(self) -> IChartSeriesGroup:
        """Returns parent series group. Read-only ."""
        ...

    @property
    def order(self) -> int:
        """Returns the order of a series. Read/write ."""
        ...

    @order.setter
    def order(self, value: int):
        ...

    @property
    def labels(self) -> IDataLabelCollection:
        """Returns the Labels of a series. Read-only ."""
        ...

    @property
    def trend_lines(self) -> ITrendlineCollection:
        """Collection of series trend lines Read-only ."""
        ...

    @property
    def error_bars_x_format(self) -> IErrorBarsFormat:
        """Represents ErrorBars of series with derection X. ErrorBars with X direction are avalible for series of type area, bar, scatter and bubble. For any other types of chart this property returns null (including 3D charts). In case of custom values use DataPoints collection to specify value (with property). Read-only ."""
        ...

    @property
    def error_bars_y_format(self) -> IErrorBarsFormat:
        """Represents ErrorBars of series with derection Y. ErrorBars with Y direction are avalible for series of type area, bar, line, scatter and bubble. For any other types of chart this property returns null (including 3D charts). In case of custom values use DataPoints collection to specify value (with property). Read-only ."""
        ...

    @property
    def plot_on_second_axis(self) -> bool:
        """Indicates if this series is plotted on second value axis. Read/write ."""
        ...

    @plot_on_second_axis.setter
    def plot_on_second_axis(self, value: bool):
        ...

    @property
    def bubble_size_scale(self) -> int:
        """Specifies the scale factor for the bubble chart (can be between 0 and 300 percents of the default size). This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.BubbleSizeScale read/write property for change value."""
        ...

    @property
    def gap_width(self) -> int:
        """Specifies the space between bar or column clusters, as a percentage of the bar or column width. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.GapWidth read/write property for change value. Read-only ."""
        ...

    @property
    def gap_depth(self) -> int:
        """Returns or sets the distance, as a percentage of the marker width, between the data series in a 3D chart. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.GapDepth read/write property for change value. Read-only ."""
        ...

    @property
    def is_color_varied(self) -> bool:
        """Specifies that each data marker in the series has a different color. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.IsColorVaried read/write property for change value. Read-only ."""
        ...

    @property
    def has_series_lines(self) -> bool:
        """Determines whether there are series lines for this series and kindred series. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.HasSeriesLines read/write property for change value. Use ParentSeriesGroup.SeriesLinesFormat property for format series lines. Read-only ."""
        ...

    @property
    def overlap(self) -> int:
        """Specifies how much bars and columns overlap on 2-D charts, as a percentage (from -100% to 100%). This is the property not only of this series but of all series of parent series group. It is a projection of the appropriate property in the parent series group, and so this property is read-only. To change the value, use the ParentSeriesGroup.Overlap read/write property. Read-only ."""
        ...

    @property
    def second_pie_size(self) -> int:
        """Specifies the size of the second pie or bar of a pie-of-pie chart or a bar-of-pie chart, as a percentage of the size of the first pie (can be between 5 and 200 percents). This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.SecondPieSize read/write property for change value. Read-only ."""
        ...

    @property
    def pie_split_position(self) -> float:
        """Specifies a value that shall be used to determine which data points are in the second pie or bar on a pie-of-pie or bar-of-pie chart. Is used together with PieSplitBy property. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.PieSplitPosition read/write property for change value. Read-only ."""
        ...

    @property
    def pie_split_by(self) -> PieSplitType:
        """Specifies how to determine which data points are in the second pie or bar on a pie-of-pie or bar-of-pie chart. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.PieSplitBy read/write property for change value. Read-only ."""
        ...

    @property
    def doughnut_hole_size(self) -> int:
        """Specifies the size of the hole in a doughnut chart (can be between 10 and 90 percents of the size of the plot area.). This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.DoughnutHoleSize read/write property for change value. Read-only ."""
        ...

    @property
    def first_slice_angle(self) -> int:
        """Specifies the angle of the first pie or doughnut chart slice, in degrees (clockwise from up, from 0 to 360 degrees). This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.FirstSliceAngle read/write property for change value. Read-only ."""
        ...

    @property
    def bubble_size_representation(self) -> BubbleSizeRepresentationType:
        """Specifies how the bubble size values are represented on the bubble chart. This is the property not only of this series but of all series of parent series group - this is projection of appropriate group property. And so this property is read-only. Use ParentSeriesGroup property for access to parent series group. Use ParentSeriesGroup.BubbleSizeRepresentation read/write property for change value."""
        ...
