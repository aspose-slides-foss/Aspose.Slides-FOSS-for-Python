from __future__ import annotations
from typing import TYPE_CHECKING
from .IBaseChartValue import IBaseChartValue

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType


class BaseChartValue(IBaseChartValue):
    """Base class for chart value types."""

    @property
    def data_source_type(self) -> DataSourceType:
        return self._data_source_type

    @data_source_type.setter
    def data_source_type(self, value: DataSourceType):
        self._data_source_type = value

    @property
    def data(self) -> object:
        return self._data

    @data.setter
    def data(self, value: object):
        self._data = value

    def _init_internal(self, data_source_type: 'DataSourceType', data: object = None):
        self._data_source_type = data_source_type
        self._data = data
