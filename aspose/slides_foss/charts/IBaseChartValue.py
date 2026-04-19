from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType

class IBaseChartValue(ABC):
    """Represents a value of a chart."""
    @property
    def data_source_type(self) -> DataSourceType:
        """Specifies whether AsCell or AsLiteralString or AsLiteralDouble property is actual. In other words it specifies the type of value of the Data property. This property is read-only. For changing value of this property you can use one of the ChartDataPointCollection.DataSourceTypeFor<...> properties. Read/write ."""
        ...

    @data_source_type.setter
    def data_source_type(self, value: DataSourceType):
        ...

    @property
    def data(self) -> object:
        """Read/write ."""
        ...

    @data.setter
    def data(self, value: object):
        ...
