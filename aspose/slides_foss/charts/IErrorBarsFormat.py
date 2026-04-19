from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IChartComponent import IChartComponent

if TYPE_CHECKING:
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from .ErrorBarType import ErrorBarType
    from .ErrorBarValueType import ErrorBarValueType
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IFormat import IFormat
    from ..IPresentation import IPresentation

class IErrorBarsFormat(IChartComponent, ABC):
    """Represents error bars of chart series. ErrorBars custom values are in IChartDataPointCollection (in property)."""
    @property
    def type(self) -> ErrorBarType:
        """Gets or sets type of error bars. Read/write ."""
        ...

    @type.setter
    def type(self, value: ErrorBarType):
        ...

    @property
    def value_type(self) -> ErrorBarValueType:
        """Represents possible ways to determine the length of the error bars. In case of custom value type to specify value use property of specific data point in DataPoints collection of series. Read/write ."""
        ...

    @value_type.setter
    def value_type(self, value: ErrorBarValueType):
        ...

    @property
    def has_end_cap(self) -> bool:
        """Specifies an end cap is not drawn on the error bars. Read/write ."""
        ...

    @has_end_cap.setter
    def has_end_cap(self, value: bool):
        ...

    @property
    def value(self) -> float:
        """Gets or sets value which is used with Fixed, Percentage and StandardDeviation value types to determine the length of the error bars. Read/write ."""
        ...

    @value.setter
    def value(self, value: float):
        ...

    @property
    def is_visible(self) -> bool:
        """Gets or sets Error Bars visibility. Read/write ."""
        ...

    @is_visible.setter
    def is_visible(self, value: bool):
        ...
