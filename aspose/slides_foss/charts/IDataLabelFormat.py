from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFormattedTextContainer import IFormattedTextContainer

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartTextFormat import IChartTextFormat
    from .IFormat import IFormat
    from ..IPresentation import IPresentation
    from .LegendDataLabelPosition import LegendDataLabelPosition

class IDataLabelFormat(IFormattedTextContainer, ABC):
    """Represents formatting options for DataLabel."""
    @property
    def is_number_format_linked_to_source(self) -> bool:
        """Read/write ."""
        ...

    @is_number_format_linked_to_source.setter
    def is_number_format_linked_to_source(self, value: bool):
        ...

    @property
    def number_format(self) -> str:
        """Represents the format string for the DataLabels object. Read/write ."""
        ...

    @number_format.setter
    def number_format(self, value: str):
        ...

    @property
    def format(self) -> IFormat:
        """Represents the format of the data label. Read-only ."""
        ...

    @property
    def position(self) -> LegendDataLabelPosition:
        """Represents the position of the data label. Read/write ."""
        ...

    @position.setter
    def position(self, value: LegendDataLabelPosition):
        ...

    @property
    def show_legend_key(self) -> bool:
        """Represents a specified chart's data label legend key display behavior. True if the data label legend key is visible. Read/write ."""
        ...

    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        ...

    @property
    def show_value(self) -> bool:
        """Represents a specified chart's data label percentage value display behavior. True displays the percentage value. False to hide. Read/write ."""
        ...

    @show_value.setter
    def show_value(self, value: bool):
        ...

    @property
    def show_category_name(self) -> bool:
        """Represents a specified chart's data label category name display behavior. True to display the category name for the data labels on a chart. False to hide. Read/write ."""
        ...

    @show_category_name.setter
    def show_category_name(self, value: bool):
        ...

    @property
    def show_series_name(self) -> bool:
        """Returns or sets a Boolean to indicate the series name display behavior for the data labels on a chart. True to show the series name. False to hide. Read/write ."""
        ...

    @show_series_name.setter
    def show_series_name(self, value: bool):
        ...

    @property
    def show_percentage(self) -> bool:
        """Represents a specified chart's data label percentage value display behavior. True displays the percentage value. False to hide. Read/write ."""
        ...

    @show_percentage.setter
    def show_percentage(self, value: bool):
        ...

    @property
    def show_bubble_size(self) -> bool:
        """Represents a specified chart's data label bubble size value display behavior. True displays the bubble size value. False to hide. Read/write ."""
        ...

    @show_bubble_size.setter
    def show_bubble_size(self, value: bool):
        ...

    @property
    def show_leader_lines(self) -> bool:
        """Represents a specified chart's data label leader lines display behavior. True displays the leader lines. False to hide. Read/write ."""
        ...

    @show_leader_lines.setter
    def show_leader_lines(self, value: bool):
        ...

    @property
    def show_label_value_from_cell(self) -> bool:
        """Represents a specified chart's data label cell value display behavior. True displays cell value. False to hide. Read/write ."""
        ...

    @show_label_value_from_cell.setter
    def show_label_value_from_cell(self, value: bool):
        ...

    @property
    def separator(self) -> str:
        """Sets or returns a Variant representing the separator used for the data labels on a chart. Read/write ."""
        ...

    @separator.setter
    def separator(self, value: str):
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...
