from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .BubbleSizeRepresentationType import BubbleSizeRepresentationType
    from .CombinableSeriesTypesGroup import CombinableSeriesTypesGroup
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartLinesFormat import IChartLinesFormat
    from .IChartSeriesReadonlyCollection import IChartSeriesReadonlyCollection
    from .IPieSplitCustomPointCollection import IPieSplitCustomPointCollection
    from ..IPresentation import IPresentation
    from .IUpDownBarsManager import IUpDownBarsManager
    from .PieSplitType import PieSplitType

class IChartSeriesGroup(IChartComponent, ABC):
    """Represents group of series."""
    @property
    def type(self) -> CombinableSeriesTypesGroup:
        """Returns a type of this series group. Read-only ."""
        ...

    @property
    def plot_on_second_axis(self) -> bool:
        """Indicates if series of this group is plotted on secondary axis. Read-only ."""
        ...

    @property
    def series(self) -> IChartSeriesReadonlyCollection:
        """Returns a readonly collection of chart series. Read-only ."""
        ...

    @property
    def gap_width(self) -> int:
        """Specifies the space between bar or column clusters, as a percentage of the bar or column width. Read/write ."""
        ...

    @gap_width.setter
    def gap_width(self, value: int):
        ...

    @property
    def gap_depth(self) -> int:
        """Returns or sets the distance, as a percentage of the marker width, between the data series in a 3D chart. Read/write ."""
        ...

    @gap_depth.setter
    def gap_depth(self, value: int):
        ...

    @property
    def first_slice_angle(self) -> int:
        """Gets or sets the angle of the first pie or doughnut chart slice, in degrees (clockwise from up, from 0 to 360 degrees). Read/write ."""
        ...

    @first_slice_angle.setter
    def first_slice_angle(self, value: int):
        ...

    @property
    def is_color_varied(self) -> bool:
        """Specifies that each data marker in the series has a different color. Read/write ."""
        ...

    @is_color_varied.setter
    def is_color_varied(self, value: bool):
        ...

    @property
    def has_series_lines(self) -> bool:
        """True if chart has series lines. Applied to stacked bar and OfPie charts. Read/write ."""
        ...

    @has_series_lines.setter
    def has_series_lines(self, value: bool):
        ...

    @property
    def overlap(self) -> int:
        """Specifies how much bars and columns shall overlap on 2-D charts, as a percentage (from -100% to 100%). - -100%: Maximum spacing (bars are completely separated). - 0%: Bars are placed side by side without overlap or spacing. - 100%: Maximum overlap (bars completely overlap each other). This property is read/write ."""
        ...

    @overlap.setter
    def overlap(self, value: int):
        ...

    @property
    def second_pie_size(self) -> int:
        """Specifies the size of the second pie or bar of a pie-of-pie chart or a bar-of-pie chart, as a percentage of the size of the first pie (can be between 5 and 200 percents). Read/write ."""
        ...

    @second_pie_size.setter
    def second_pie_size(self, value: int):
        ...

    @property
    def pie_split_position(self) -> float:
        """Specifies a value that shall be used to determine which data points are in the second pie or bar on a pie-of-pie or bar-of-pie chart. Is used together with PieSplitBy property. Read/write ."""
        ...

    @pie_split_position.setter
    def pie_split_position(self, value: float):
        ...

    @property
    def pie_split_by(self) -> PieSplitType:
        """Specifies how to determine which data points are in the second pie or bar on a pie-of-pie or bar-of-pie chart. Read/write ."""
        ...

    @pie_split_by.setter
    def pie_split_by(self, value: PieSplitType):
        ...

    @property
    def doughnut_hole_size(self) -> int:
        """Specifies the size of the hole in a doughnut chart (can be between 10 and 90 percents of the size of the plot area.). Read/write ."""
        ...

    @doughnut_hole_size.setter
    def doughnut_hole_size(self, value: int):
        ...

    @property
    def bubble_size_scale(self) -> int:
        """Specifies the scale factor for the bubble chart (can be between 0 and 300 percents of the default size). Read/write ."""
        ...

    @bubble_size_scale.setter
    def bubble_size_scale(self, value: int):
        ...

    @property
    def bubble_size_representation(self) -> BubbleSizeRepresentationType:
        """Specifies how the bubble size values are represented on the bubble chart. Read/write ."""
        ...

    @bubble_size_representation.setter
    def bubble_size_representation(self, value: BubbleSizeRepresentationType):
        ...
