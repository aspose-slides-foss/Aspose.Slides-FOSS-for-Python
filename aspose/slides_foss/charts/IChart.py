from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from ..IGraphicalObject import IGraphicalObject
from .IFormattedTextContainer import IFormattedTextContainer
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..BlackWhiteMode import BlackWhiteMode
    from .ChartType import ChartType
    from .DisplayBlanksAsType import DisplayBlanksAsType
    from .IAxesManager import IAxesManager
    from ..IBaseSlide import IBaseSlide
    from .IChartData import IChartData
    from .IChartPlotArea import IChartPlotArea
    from .IChartTextFormat import IChartTextFormat
    from .IChartTitle import IChartTitle
    from .IChartWall import IChartWall
    from ..ICustomData import ICustomData
    from .IDataTable import IDataTable
    from ..IEffectFormat import IEffectFormat
    from ..IFillFormat import IFillFormat
    from ..IGraphicalObjectLock import IGraphicalObjectLock
    from ..IGroupShape import IGroupShape
    from ..IHyperlink import IHyperlink
    from ..IHyperlinkManager import IHyperlinkManager
    from ..IImage import IImage
    from .ILegend import ILegend
    from ..ILineFormat import ILineFormat
    from ..theme.IOverrideThemeManager import IOverrideThemeManager
    from ..IPlaceholder import IPlaceholder
    from ..IPresentation import IPresentation
    from .IRotation3D import IRotation3D
    from ..IShapeFrame import IShapeFrame
    from ..theme.IThemeEffectiveData import IThemeEffectiveData
    from ..IThreeDFormat import IThreeDFormat
    from .StyleType import StyleType

class IChart(IGraphicalObject, IFormattedTextContainer, IChartComponent, ABC):
    """Represents an graphic chart on a slide."""
    @property
    def plot_visible_cells_only(self) -> bool:
        """Determines whether the only visible cells are plotted. False to plot both visible and hidden cells. Read/write ."""
        ...

    @plot_visible_cells_only.setter
    def plot_visible_cells_only(self, value: bool):
        ...

    @property
    def display_blanks_as(self) -> DisplayBlanksAsType:
        """Returns or sets the way to plot blank cells on a chart. Read/write ."""
        ...

    @display_blanks_as.setter
    def display_blanks_as(self, value: DisplayBlanksAsType):
        ...

    @property
    def chart_data(self) -> IChartData:
        """Returns information about the linked or embedded data associated with a chart. Read-only ."""
        ...

    @property
    def has_title(self) -> bool:
        """Determines whether a chart has a visible title. Read/write ."""
        ...

    @has_title.setter
    def has_title(self, value: bool):
        ...

    @property
    def chart_title(self) -> IChartTitle:
        """Returns or sets a chart title Read-only ."""
        ...

    @property
    def has_data_table(self) -> bool:
        """Determines whether a chart has a data table. Read/write ."""
        ...

    @has_data_table.setter
    def has_data_table(self, value: bool):
        ...

    @property
    def has_legend(self) -> bool:
        """Determines whether a chart has a legend. Read/write ."""
        ...

    @has_legend.setter
    def has_legend(self, value: bool):
        ...

    @property
    def legend(self) -> ILegend:
        """Returns or sets a legend for a chart. Read-only ."""
        ...

    @property
    def chart_data_table(self) -> IDataTable:
        """Returns a data table of a chart. Read-only ."""
        ...

    @property
    def style(self) -> StyleType:
        """Returns or sets the chart style. Read/write ."""
        ...

    @style.setter
    def style(self, value: StyleType):
        ...

    @property
    def type(self) -> ChartType:
        """Returns or sets the chart type. Read/write ."""
        ...

    @type.setter
    def type(self, value: ChartType):
        ...

    @property
    def plot_area(self) -> IChartPlotArea:
        """Represents the plot area of a chart. Read-only ."""
        ...

    @property
    def rotation_3d(self) -> IRotation3D:
        """Returns a 3D rotation of a chart. Read-only ."""
        ...

    @property
    def back_wall(self) -> IChartWall:
        """Returns an object which allows to change format of the back wall of a 3D chart. Read-only ."""
        ...

    @property
    def side_wall(self) -> IChartWall:
        """Returns an object which allows to change format of the side wall of a 3D chart. Read-only ."""
        ...

    @property
    def floor(self) -> IChartWall:
        """Returns an object which allows to change format of the floor of a 3D chart. Read-only ."""
        ...

    @property
    def axes(self) -> IAxesManager:
        """Provide access to chart axes. Read-only ."""
        ...

    @property
    def show_data_labels_over_maximum(self) -> bool:
        """Specifies data labels over the maximum of the chart shall be shown. Read/write ."""
        ...

    @show_data_labels_over_maximum.setter
    def show_data_labels_over_maximum(self, value: bool):
        ...

    @property
    def has_rounded_corners(self) -> bool:
        """Specifies the chart area shall have rounded corners. Read/write ."""
        ...

    @has_rounded_corners.setter
    def has_rounded_corners(self, value: bool):
        ...

    @property
    def line_format(self) -> ILineFormat:
        ...

    @property
    def three_d_format(self) -> IThreeDFormat:
        ...

    @property
    def effect_format(self) -> IEffectFormat:
        ...

    @property
    def fill_format(self) -> IFillFormat:
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...

    @property
    def chart(self) -> IChart:
        ...

    def validate_chart_layout(self) -> None:
        ...
