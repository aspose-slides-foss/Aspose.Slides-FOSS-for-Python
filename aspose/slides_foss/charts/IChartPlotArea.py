from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ILayoutable import ILayoutable
from .IActualLayout import IActualLayout

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IFormat import IFormat
    from ..IPresentation import IPresentation
    from .LayoutTargetType import LayoutTargetType

class IChartPlotArea(ILayoutable, IActualLayout, ABC):
    """Represents chart title properties."""
    @property
    def format(self) -> IFormat:
        """Returns the format of a plot area. Read-only ."""
        ...

    @property
    def as_i_layoutable(self) -> ILayoutable:
        """Allows to get base ILayoutable interface. Read-only ."""
        ...

    @property
    def as_i_actual_layout(self) -> IActualLayout:
        """Returns IActualLayout interface."""
        ...

    @property
    def layout_target_type(self) -> LayoutTargetType:
        """If layout of the plot area defined manually this property specifies whether to layout the plot area by its inside (not including axis and axis labels) or outside (including axis and axis labels). Read/write ."""
        ...

    @layout_target_type.setter
    def layout_target_type(self, value: LayoutTargetType):
        ...

    @property
    def x(self) -> float:
        ...

    @x.setter
    def x(self, value: float):
        ...

    @property
    def y(self) -> float:
        ...

    @y.setter
    def y(self, value: float):
        ...

    @property
    def width(self) -> float:
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def height(self) -> float:
        ...

    @height.setter
    def height(self, value: float):
        ...

    @property
    def right(self) -> float:
        ...

    @property
    def bottom(self) -> float:
        ...

    @property
    def as_i_chart_component(self) -> IChartComponent:
        ...

    @property
    def chart(self) -> IChart:
        ...

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        ...

    @property
    def slide(self) -> IBaseSlide:
        ...

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        ...

    @property
    def presentation(self) -> IPresentation:
        ...

    @property
    def actual_x(self) -> float:
        ...

    @property
    def actual_y(self) -> float:
        ...

    @property
    def actual_width(self) -> float:
        ...

    @property
    def actual_height(self) -> float:
        ...
