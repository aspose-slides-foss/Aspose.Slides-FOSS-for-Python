from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IOverridableText import IOverridableText

if TYPE_CHECKING:
    from .IFormattedTextContainer import IFormattedTextContainer
    from .IChartComponent import IChartComponent
    from ..ISlideComponent import ISlideComponent
    from ..IPresentationComponent import IPresentationComponent
    from ..IBaseSlide import IBaseSlide
    from .IChart import IChart
    from .IChartTextFormat import IChartTextFormat
    from .IFormat import IFormat
    from .ILegendEntryProperties import ILegendEntryProperties
    from ..IPresentation import IPresentation
    from ..ITextFrame import ITextFrame
    from .TrendlineType import TrendlineType

class ITrendline(IOverridableText, ABC):
    """Class represents trend line of chart series"""
    @property
    def trendline_name(self) -> str:
        """Gets or sets name of the trendline. Read/write ."""
        ...

    @trendline_name.setter
    def trendline_name(self, value: str):
        ...

    @property
    def trendline_type(self) -> TrendlineType:
        """Gets or sets type of trend line. Read/write ."""
        ...

    @trendline_type.setter
    def trendline_type(self, value: TrendlineType):
        ...

    @property
    def backward(self) -> float:
        """Specifies the number of categories (or units on a scatter chart) that the trend line extends before the data for the series that is being trended. On scatter and non-scatter charts, the value shall be any nonnegative value. Read/write ."""
        ...

    @backward.setter
    def backward(self, value: float):
        ...

    @property
    def forward(self) -> float:
        """Specifies the number of categories (or units on a scatter chart) that the trendline extends after the data for the series that is being trended. On scatter and non-scatter charts, the value shall be any non-negative value. Read/write ."""
        ...

    @forward.setter
    def forward(self, value: float):
        ...

    @property
    def intercept(self) -> float:
        """Specifies the value where the trendline shall cross the y axis. This property shall be supported only when the trendline type is exp, linear, or poly. Read/write ."""
        ...

    @intercept.setter
    def intercept(self, value: float):
        ...

    @property
    def display_equation(self) -> bool:
        """Specifies that the equation for the trendline is displayed on the chart (in the same label as the Rsquaredvalue). Read/write ."""
        ...

    @display_equation.setter
    def display_equation(self, value: bool):
        ...

    @property
    def order(self) -> int:
        """Specifies the order of the polynomial trend line. It is ignored for other trend line types. Value must be between 2 and 6. Read/write ."""
        ...

    @order.setter
    def order(self, value: int):
        ...

    @property
    def period(self) -> int:
        """Specifies the period of the trend line for a moving average trend line. It is ignored for other trend line variants. Value must be between 2 and 255. Read/write ."""
        ...

    @period.setter
    def period(self, value: int):
        ...

    @property
    def display_r_squared_value(self) -> bool:
        """Specifies that the R-squared value of the trendline is displayed on the chart (in the same label as the equation). Read/write ."""
        ...

    @display_r_squared_value.setter
    def display_r_squared_value(self, value: bool):
        ...
