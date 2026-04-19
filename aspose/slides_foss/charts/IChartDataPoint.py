from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IActualLayout import IActualLayout

if TYPE_CHECKING:
    from ..drawing import Color
    from .IDataLabel import IDataLabel
    from .IDoubleChartValue import IDoubleChartValue
    from .IErrorBarsCustomValues import IErrorBarsCustomValues
    from .IFormat import IFormat
    from .ILegendEntryProperties import ILegendEntryProperties
    from .IMarker import IMarker
    from .IStringOrDoubleChartValue import IStringOrDoubleChartValue

class IChartDataPoint(IActualLayout, ABC):
    """Represents series data point."""
    @property
    def x_value(self) -> IStringOrDoubleChartValue:
        """Returns the x value of chart data point. Read-only ."""
        ...

    @property
    def y_value(self) -> IDoubleChartValue:
        """Returns the y value of chart data point. Read-only ."""
        ...

    @property
    def bubble_size(self) -> IDoubleChartValue:
        """Returns the bubble size of chart data point. Read-only ."""
        ...

    @property
    def value(self) -> IDoubleChartValue:
        """Returns the value of chart data point. Read-only ."""
        ...

    @property
    def error_bars_custom_values(self) -> IErrorBarsCustomValues:
        """Represents series error bars values in case of Custom value type. Read-only ."""
        ...

    @property
    def label(self) -> IDataLabel:
        """Represents the lable of chart data point. Read-only ."""
        ...

    @property
    def marker(self) -> IMarker:
        """Specifies a data marker. Read-only ."""
        ...

    @property
    def index(self) -> int:
        """Determines which of the parent's children collection this data point applies to. Read ."""
        ...

    def remove(self) -> None:
        ...
