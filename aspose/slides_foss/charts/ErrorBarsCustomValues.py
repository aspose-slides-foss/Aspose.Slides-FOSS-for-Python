from __future__ import annotations
from typing import TYPE_CHECKING
from .IErrorBarsCustomValues import IErrorBarsCustomValues

if TYPE_CHECKING:
    from .DoubleChartValue import DoubleChartValue
    from .IDoubleChartValue import IDoubleChartValue


class ErrorBarsCustomValues(IErrorBarsCustomValues):
    """Specifies the error bar values for a single data point.

    Used only when the error bars value type is Custom.
    """

    @property
    def x_minus(self) -> IDoubleChartValue:
        return self._x_minus

    @property
    def y_minus(self) -> IDoubleChartValue:
        return self._y_minus

    @property
    def x_plus(self) -> IDoubleChartValue:
        return self._x_plus

    @property
    def y_plus(self) -> IDoubleChartValue:
        return self._y_plus

    def _init_internal(self):
        from .DoubleChartValue import DoubleChartValue
        from .DataSourceType import DataSourceType

        self._x_minus = DoubleChartValue()
        self._x_minus._init_internal(DataSourceType.DOUBLE_LITERALS, literal=0.0)
        self._x_plus = DoubleChartValue()
        self._x_plus._init_internal(DataSourceType.DOUBLE_LITERALS, literal=0.0)
        self._y_minus = DoubleChartValue()
        self._y_minus._init_internal(DataSourceType.DOUBLE_LITERALS, literal=0.0)
        self._y_plus = DoubleChartValue()
        self._y_plus._init_internal(DataSourceType.DOUBLE_LITERALS, literal=0.0)
