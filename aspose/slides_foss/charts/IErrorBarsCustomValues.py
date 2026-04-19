from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IDoubleChartValue import IDoubleChartValue

class IErrorBarsCustomValues(ABC):
    """Specifies the errors bar values. It shall be used only when the Error bars value type is Custom."""
    @property
    def x_minus(self) -> IDoubleChartValue:
        """Specifies the error bar value in the negative direction. Avalible if error bars value type is Custom and ErrorBarsXFormat is allowed. In any other case this property returns null. Read-only ."""
        ...

    @property
    def y_minus(self) -> IDoubleChartValue:
        """Specifies the error bar value in the negative direction. Avalible if error bars value type is Custom and ErrorBarsYFormat is allowed. In any other case this property returns null. Read-only ."""
        ...

    @property
    def x_plus(self) -> IDoubleChartValue:
        """Specifies the error bar value in the positive direction. Avalible if error bars value type is Custom and ErrorBarsXFormat is allowed. In any other case this property returns null. Read-only ."""
        ...

    @property
    def y_plus(self) -> IDoubleChartValue:
        """Specifies the error bar value in the positive direction. Avalible if error bars value type is Custom and ErrorBarsYFormat is allowed. In any other case this property returns null. Read-only ."""
        ...
