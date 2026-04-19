from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ILayoutable import ILayoutable
from .IOverridableText import IOverridableText
from .IFormattedTextContainer import IFormattedTextContainer
from .IActualLayout import IActualLayout

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartTextFormat import IChartTextFormat
    from .IFormat import IFormat
    from ..IPresentation import IPresentation
    from ..IPresentationComponent import IPresentationComponent
    from ..ITextFrame import ITextFrame

class IChartTitle(ILayoutable, IOverridableText, IFormattedTextContainer, IActualLayout, ABC):
    """Represents chart title properties."""
    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap title. Read/write ."""
        ...

    @overlay.setter
    def overlay(self, value: bool):
        ...

    @property
    def format(self) -> IFormat:
        """Returns the fill, line, effect styles of a title. Read-only ."""
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
    def text_frame_for_overriding(self) -> ITextFrame:
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...

    def add_text_frame_for_overriding(self, text) -> ITextFrame:
        ...
