from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartTextFormat import IChartTextFormat
    from ..IPresentation import IPresentation

class IFormattedTextContainer(IChartComponent, ABC):
    """Represents chart text format."""
    @property
    def text_format(self) -> IChartTextFormat:
        """Returns chart text format. Read-only ."""
        ...

    @property
    def as_i_chart_component(self) -> IChartComponent:
        """Returns IChartComponent interface. Read-only ."""
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

