from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType

class IDataSourceTypeForErrorBarsCustomValues(ABC):
    """Specifies types of values in ChartDataPoint.ErrorBarsCustomValues properties list"""
    @property
    def data_source_type_for_x_minus_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points XMinus property object for error bars custom values. In other words it specifies the type of value of ChartDataPoint.ErrorBarsCustomValues.XMinus.Data property. Read/write ."""
        ...

    @data_source_type_for_x_minus_values.setter
    def data_source_type_for_x_minus_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_x_plus_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points XPlus property object for error bars custom values. In other words it specifies the type of value of ChartDataPoint.ErrorBarsCustomValues.XPlus.Data property. Read/write ."""
        ...

    @data_source_type_for_x_plus_values.setter
    def data_source_type_for_x_plus_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_y_minus_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points YMinus property object for error bars custom values. In other words it specifies the type of value of ChartDataPointEx.ErrorBarsCustomValues.YMinus.Data property. Read/write ."""
        ...

    @data_source_type_for_y_minus_values.setter
    def data_source_type_for_y_minus_values(self, value: DataSourceType):
        ...

    @property
    def data_source_type_for_y_plus_values(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual in data points YPlus property object for error bars custom values. In other words it specifies the type of value of ChartDataPointEx.ErrorBarsCustomValues.YPlus.Data property. Read/write ."""
        ...

    @data_source_type_for_y_plus_values.setter
    def data_source_type_for_y_plus_values(self, value: DataSourceType):
        ...
