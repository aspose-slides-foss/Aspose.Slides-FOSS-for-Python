from __future__ import annotations
from typing import TYPE_CHECKING

from .DataSourceType import DataSourceType
from .IDataSourceTypeForErrorBarsCustomValues import IDataSourceTypeForErrorBarsCustomValues


class DataSourceTypeForErrorBarsCustomValues(IDataSourceTypeForErrorBarsCustomValues):
    """Specifies types of values in ChartDataPoint.ErrorBarsCustomValues properties list."""

    @property
    def data_source_type_for_x_minus_values(self) -> DataSourceType:
        return self._x_minus

    @data_source_type_for_x_minus_values.setter
    def data_source_type_for_x_minus_values(self, value: DataSourceType):
        self._x_minus = value

    @property
    def data_source_type_for_x_plus_values(self) -> DataSourceType:
        return self._x_plus

    @data_source_type_for_x_plus_values.setter
    def data_source_type_for_x_plus_values(self, value: DataSourceType):
        self._x_plus = value

    @property
    def data_source_type_for_y_minus_values(self) -> DataSourceType:
        return self._y_minus

    @data_source_type_for_y_minus_values.setter
    def data_source_type_for_y_minus_values(self, value: DataSourceType):
        self._y_minus = value

    @property
    def data_source_type_for_y_plus_values(self) -> DataSourceType:
        return self._y_plus

    @data_source_type_for_y_plus_values.setter
    def data_source_type_for_y_plus_values(self, value: DataSourceType):
        self._y_plus = value

    def _init_internal(self):
        self._x_minus = DataSourceType.DOUBLE_LITERALS
        self._x_plus = DataSourceType.DOUBLE_LITERALS
        self._y_minus = DataSourceType.DOUBLE_LITERALS
        self._y_plus = DataSourceType.DOUBLE_LITERALS
