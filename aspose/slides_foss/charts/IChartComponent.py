from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from ..IPresentation import IPresentation

class IChartComponent(ISlideComponent, IPresentationComponent, ABC):
    """Represents a component of a chart."""
    @property
    def chart(self) -> IChart:
        """Returns the chart. Read-only ."""
        ...

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
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

