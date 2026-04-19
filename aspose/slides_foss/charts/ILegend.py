from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ILayoutable import ILayoutable
from .IFormattedTextContainer import IFormattedTextContainer
from .IActualLayout import IActualLayout

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartTextFormat import IChartTextFormat
    from .IFormat import IFormat
    from .ILegendEntryCollection import ILegendEntryCollection
    from ..IPresentation import IPresentation
    from .LegendPositionType import LegendPositionType

class ILegend(ILayoutable, IFormattedTextContainer, IActualLayout, ABC):
    """Represents chart's legend properties."""
    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap legend. Read/write ."""
        ...

    @overlay.setter
    def overlay(self, value: bool):
        ...

    @property
    def position(self) -> LegendPositionType:
        """Specifies the position of the legend on a chart. Non-NaN values of X, Y, Width, Heigt properties override effect of this property. Read/write ."""
        ...

    @position.setter
    def position(self, value: LegendPositionType):
        ...

    @property
    def format(self) -> IFormat:
        """Returns the format of a legend. Read-only ."""
        ...

    @property
    def entries(self) -> ILegendEntryCollection:
        """Gets legend entries. Read-only ."""
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
    def chart(self) -> IChart:
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...
