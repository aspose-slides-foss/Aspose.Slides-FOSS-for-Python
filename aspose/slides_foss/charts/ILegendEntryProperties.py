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
    from ..IPresentation import IPresentation

class ILegendEntryProperties(IFormattedTextContainer, ABC):
    """Represents legend properties of a chart."""
    @property
    def hide(self) -> bool:
        """Returns or sets the hide flag of legend entry. Read/write ."""
        ...

    @hide.setter
    def hide(self, value: bool):
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...
