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
    from ..ITextFrame import ITextFrame

class IOverridableText(IFormattedTextContainer, ABC):
    """Represents overridable text for a chart."""
    @property
    def text_frame_for_overriding(self) -> ITextFrame:
        """Can contain a rich formatted text. If this property is not null then this formatted text value overrides auto-generated text. Auto-generated text is an implicit property of the data label, the display unit label of the value axis, the axis title, the chart title, the label of the trendline. Auto-generated text is formatted with the IFormattedTextContainer.TextFormat property. Read-only ."""
        ...


    @property
    def text_format(self) -> IChartTextFormat:
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
    def add_text_frame_for_overriding(self, text) -> ITextFrame:
        ...

