from __future__ import annotations
from abc import ABC, abstractmethod

class IActualLayout(ABC):
    """Specifies actual position of a chart element."""
    @property
    def actual_x(self) -> float:
        """Specifies actual x location (left) of the chart element relative to the left top corner of the chart. Call method IChart.ValidateChartLayout() before to get actual values. Read ."""
        ...

    @property
    def actual_y(self) -> float:
        """Specifies actual top of the chart element relative to the left top corner of the chart. Call method IChart.ValidateChartLayout() before to get actual values. Read ."""
        ...

    @property
    def actual_width(self) -> float:
        """Specifies actual width of the chart element. Call method IChart.ValidateChartLayout() before to get actual values. Read ."""
        ...

    @property
    def actual_height(self) -> float:
        """Specifies actual height of the chart element. Call method IChart.ValidateChartLayout() before to get actual values. Read ."""
        ...

