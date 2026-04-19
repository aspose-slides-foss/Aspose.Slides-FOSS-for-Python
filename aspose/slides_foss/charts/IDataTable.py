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

class IDataTable(IFormattedTextContainer, ABC):
    """Represents data table properties."""
    @property
    def has_border_horizontal(self) -> bool:
        """True if the chart data table has horizontal cell borders. Read/write ."""
        ...

    @has_border_horizontal.setter
    def has_border_horizontal(self, value: bool):
        ...

    @property
    def has_border_outline(self) -> bool:
        """True if the chart data table has outline borders. Read/write ."""
        ...

    @has_border_outline.setter
    def has_border_outline(self, value: bool):
        ...

    @property
    def has_border_vertical(self) -> bool:
        """True if the chart data table has vertical cell borders. Read/write ."""
        ...

    @has_border_vertical.setter
    def has_border_vertical(self, value: bool):
        ...

    @property
    def show_legend_key(self) -> bool:
        """True if the data label legend key is visible. Read/write ."""
        ...

    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        ...

    @property
    def chart(self) -> IChart:
        ...
