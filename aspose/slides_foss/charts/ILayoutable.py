from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .IChart import IChart
    from ..IPresentation import IPresentation

class ILayoutable(IChartComponent, ABC):
    """Specifies the exact position of a chart element."""
    @property
    def x(self) -> float:
        """Specifies the x location (left) of the chart element as a fraction of the width of the chart. Read/write ."""
        ...

    @x.setter
    def x(self, value: float):
        ...

    @property
    def y(self) -> float:
        """Specifies the top of the chart element as a fraction of the height of the chart. Read/write ."""
        ...

    @y.setter
    def y(self, value: float):
        ...

    @property
    def width(self) -> float:
        """Specifies the width of the chart element as a fraction of the width of the chart. Read/write ."""
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def height(self) -> float:
        """Specifies the height of the chart element as a fraction of the height of the chart. Read/write ."""
        ...

    @height.setter
    def height(self, value: float):
        ...

    @property
    def right(self) -> float:
        """Gets the right of the chart element as a fraction of the width of the chart. Read-only ."""
        ...

    @property
    def bottom(self) -> float:
        """Gets the top of the chart element as a fraction of the height of the chart. Read-only ."""
        ...

    @property
    def as_i_chart_component(self) -> IChartComponent:
        """Allows to get base IChartComponent interface. Read-only ."""
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

