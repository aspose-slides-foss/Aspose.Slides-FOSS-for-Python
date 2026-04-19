from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ILayoutable import ILayoutable
from .IOverridableText import IOverridableText
from .IActualLayout import IActualLayout

if TYPE_CHECKING:
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .IFormattedTextContainer import IFormattedTextContainer
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartDataCell import IChartDataCell
    from .IChartTextFormat import IChartTextFormat
    from .IDataLabelFormat import IDataLabelFormat
    from ..IPresentation import IPresentation
    from ..ITextFrame import ITextFrame

class IDataLabel(ILayoutable, IOverridableText, IActualLayout, ABC):
    """Represents a series labels."""
    @property
    def is_visible(self) -> bool:
        """False means that data label is not visible (and so all Show*-flags (ShowValue, ...) are false). Read-only ."""
        ...

    @property
    def data_label_format(self) -> IDataLabelFormat:
        """Returns format of the data label. Read-only ."""
        ...

    @property
    def value_from_cell(self) -> IChartDataCell:
        """Gets or sets workbook data cell. Applied if IDataLabelFormat.ShowLabelValueFromCell property equals true."""
        ...

    @value_from_cell.setter
    def value_from_cell(self, value: IChartDataCell):
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
    def slide(self) -> IBaseSlide:
        ...

    @property
    def presentation(self) -> IPresentation:
        ...

    @property
    def text_frame_for_overriding(self) -> ITextFrame:
        ...

    @property
    def text_format(self) -> IChartTextFormat:
        ...

    def hide(self) -> None:
        ...

    def get_actual_label_text(self) -> str:
        ...

    def add_text_frame_for_overriding(self, text) -> ITextFrame:
        ...
