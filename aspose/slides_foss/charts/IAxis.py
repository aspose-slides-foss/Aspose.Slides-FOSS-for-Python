from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFormattedTextContainer import IFormattedTextContainer

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .AxisPositionType import AxisPositionType
    from .CategoryAxisType import CategoryAxisType
    from .CrossesType import CrossesType
    from .DisplayUnitType import DisplayUnitType
    from .IAxisFormat import IAxisFormat
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartLinesFormat import IChartLinesFormat
    from .IChartTextFormat import IChartTextFormat
    from .IChartTitle import IChartTitle
    from ..IPresentation import IPresentation
    from .TickLabelPositionType import TickLabelPositionType
    from .TickMarkType import TickMarkType
    from .TimeUnitType import TimeUnitType

class IAxis(IFormattedTextContainer, ABC):
    """Encapsulates the object that represents a chart's axis."""
    @property
    def axis_between_categories(self) -> bool:
        """Represents if the value axis crosses the category axis between categories. This property applies only to category axes, and it doesn't apply to 3-D charts. Read/write ."""
        ...

    @axis_between_categories.setter
    def axis_between_categories(self, value: bool):
        ...

    @property
    def cross_at(self) -> float:
        """Represents the point on the axis where the perpendicular axis crosses it. Read/write ."""
        ...

    @cross_at.setter
    def cross_at(self, value: float):
        ...

    @property
    def display_unit(self) -> DisplayUnitType:
        """Specifies the scaling value of the display units for the value axis. Read/write ."""
        ...

    @display_unit.setter
    def display_unit(self, value: DisplayUnitType):
        ...

    @property
    def actual_max_value(self) -> float:
        """Specifies actual maximum value on the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def actual_min_value(self) -> float:
        """Specifies actual minimum value on the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def actual_major_unit(self) -> float:
        """Specifies actual major unit of the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def actual_minor_unit(self) -> float:
        """Specifies actual minor unit of the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def actual_major_unit_scale(self) -> TimeUnitType:
        """Specifies actual major unit scale of the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def actual_minor_unit_scale(self) -> TimeUnitType:
        """Specifies actual minor unit scale of the axis. Call method IChart.ValidateChartLayout() previously to get actual value."""
        ...

    @property
    def is_automatic_max_value(self) -> bool:
        """Indicates whether the max value is automatically assigned. Read/write ."""
        ...

    @is_automatic_max_value.setter
    def is_automatic_max_value(self, value: bool):
        ...

    @property
    def max_value(self) -> float:
        """Represents the maximum value on the value axis. Read/write ."""
        ...

    @max_value.setter
    def max_value(self, value: float):
        ...

    @property
    def minor_unit(self) -> float:
        """Represents the minor units for the date or value axis. Read/write ."""
        ...

    @minor_unit.setter
    def minor_unit(self, value: float):
        ...

    @property
    def is_automatic_minor_unit(self) -> bool:
        """Indicates whether the minor unit of the axis is automatically assigned. Read/write ."""
        ...

    @is_automatic_minor_unit.setter
    def is_automatic_minor_unit(self, value: bool):
        ...

    @property
    def major_unit(self) -> float:
        """Represents the major units for the date or value axis. Read/write ."""
        ...

    @major_unit.setter
    def major_unit(self, value: float):
        ...

    @property
    def is_automatic_major_unit(self) -> bool:
        """Indicates whether the major unit of the axis is automatically assigned. Read/write ."""
        ...

    @is_automatic_major_unit.setter
    def is_automatic_major_unit(self, value: bool):
        ...

    @property
    def is_automatic_min_value(self) -> bool:
        """Indicates whether the min value is automatically assigned. Read/write ."""
        ...

    @is_automatic_min_value.setter
    def is_automatic_min_value(self, value: bool):
        ...

    @property
    def min_value(self) -> float:
        """Represents the minimum value on the value axis. Read/write ."""
        ...

    @min_value.setter
    def min_value(self, value: float):
        ...

    @property
    def is_logarithmic(self) -> bool:
        """Represents if the value axis scale type is logarithmic or not. Read/write ."""
        ...

    @is_logarithmic.setter
    def is_logarithmic(self, value: bool):
        ...

    @property
    def log_base(self) -> float:
        """Represents the logarithmic base. Default value is 10. Read/write ."""
        ...

    @log_base.setter
    def log_base(self, value: float):
        ...

    @property
    def is_plot_order_reversed(self) -> bool:
        """Represents if MS PowerPoint plots data points from last to first. Read/write ."""
        ...

    @is_plot_order_reversed.setter
    def is_plot_order_reversed(self, value: bool):
        ...

    @property
    def is_visible(self) -> bool:
        """Represents if the axis is visible. Read/write ."""
        ...

    @is_visible.setter
    def is_visible(self, value: bool):
        ...

    @property
    def major_tick_mark(self) -> TickMarkType:
        """Represents the type of major tick mark for the specified axis. Read/write ."""
        ...

    @major_tick_mark.setter
    def major_tick_mark(self, value: TickMarkType):
        ...

    @property
    def minor_tick_mark(self) -> TickMarkType:
        """Represents the type of minor tick mark for the specified axis. Read/write ."""
        ...

    @minor_tick_mark.setter
    def minor_tick_mark(self, value: TickMarkType):
        ...

    @property
    def tick_label_position(self) -> TickLabelPositionType:
        """Represents the position of tick-mark labels on the specified axis. Read/write ."""
        ...

    @tick_label_position.setter
    def tick_label_position(self, value: TickLabelPositionType):
        ...

    @property
    def major_unit_scale(self) -> TimeUnitType:
        """Represents the major unit scale for the date axis. Read/write ."""
        ...

    @major_unit_scale.setter
    def major_unit_scale(self, value: TimeUnitType):
        ...

    @property
    def minor_unit_scale(self) -> TimeUnitType:
        """Represents the major unit scale for the date axis. Read/write ."""
        ...

    @minor_unit_scale.setter
    def minor_unit_scale(self, value: TimeUnitType):
        ...

    @property
    def base_unit_scale(self) -> TimeUnitType:
        """Specifies the smallest time unit that is represented on the date axis. Read/write ."""
        ...

    @base_unit_scale.setter
    def base_unit_scale(self, value: TimeUnitType):
        ...

    @property
    def minor_grid_lines_format(self) -> IChartLinesFormat:
        """Represents minor gridlines format on a chart axis. Read-only ."""
        ...

    @property
    def major_grid_lines_format(self) -> IChartLinesFormat:
        """Represents major gridlines format on a chart axis. Read-only ."""
        ...

    @property
    def show_minor_grid_lines(self) -> bool:
        """Represents if the minor gridlines showed. Read-only ."""
        ...

    @property
    def show_major_grid_lines(self) -> bool:
        """Represents if the major gridlines showed. Read-only ."""
        ...

    @property
    def format(self) -> IAxisFormat:
        """Represents format of axis. Read-only ."""
        ...

    @property
    def title(self) -> IChartTitle:
        """Gets the axis' title. Read-only ."""
        ...

    @property
    def cross_type(self) -> CrossesType:
        """Represents the CrossType on the specified axis where the other axis crosses. Read/write ."""
        ...

    @cross_type.setter
    def cross_type(self, value: CrossesType):
        ...

    @property
    def position(self) -> AxisPositionType:
        """Represents position of axis. Read/write ."""
        ...

    @position.setter
    def position(self, value: AxisPositionType):
        ...

    @property
    def has_title(self) -> bool:
        """Determines whether a axis has a visible title. Read/write ."""
        ...

    @has_title.setter
    def has_title(self, value: bool):
        ...

    @property
    def number_format(self) -> str:
        """Represents the format string for the Axis Labels. Read/write ."""
        ...

    @number_format.setter
    def number_format(self, value: str):
        ...

    @property
    def is_number_format_linked_to_source(self) -> bool:
        """Indicates whether the format is linked source data. Read/write ."""
        ...

    @is_number_format_linked_to_source.setter
    def is_number_format_linked_to_source(self, value: bool):
        ...

    @property
    def tick_label_rotation_angle(self) -> float:
        """Represents the rotation angle of tick labels Read/write ."""
        ...

    @tick_label_rotation_angle.setter
    def tick_label_rotation_angle(self, value: float):
        ...

    @property
    def tick_label_spacing(self) -> int:
        """Specifies how many tick labels to skip between label that is drawn. Read/write ."""
        ...

    @tick_label_spacing.setter
    def tick_label_spacing(self, value: int):
        ...

    @property
    def is_automatic_tick_label_spacing(self) -> bool:
        """Specifies automatic tick label spacing value. If false: use TickLabelSpacing property. Read/write ."""
        ...

    @is_automatic_tick_label_spacing.setter
    def is_automatic_tick_label_spacing(self, value: bool):
        ...

    @property
    def tick_marks_spacing(self) -> int:
        """Specifies how many tick marks shall be skipped before the next one shall be drawn. Applied to category or series axis. Read/write ."""
        ...

    @tick_marks_spacing.setter
    def tick_marks_spacing(self, value: int):
        ...

    @property
    def is_automatic_tick_marks_spacing(self) -> bool:
        """Specifies automatic tick marks spacing value. If false: use TickMarksSpacing property. Read/write ."""
        ...

    @is_automatic_tick_marks_spacing.setter
    def is_automatic_tick_marks_spacing(self, value: bool):
        ...

    @property
    def label_offset(self) -> int:
        """Specifies the distance of labels from the axis. Applied to category or date axis. Value must be between 0% and 1000%. Read/write ."""
        ...

    @label_offset.setter
    def label_offset(self, value: int):
        ...

    @property
    def category_axis_type(self) -> CategoryAxisType:
        """Specifies the type of the category axis. Read/write ."""
        ...

    @category_axis_type.setter
    def category_axis_type(self, value: CategoryAxisType):
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...

    def set_category_axis_type_automatically(self) -> None:
        ...
