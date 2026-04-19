from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBaseChartValue import IBaseChartValue

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType
    from .IChartCellCollection import IChartCellCollection

class IMultipleCellChartValue(IBaseChartValue, ABC):
    """Represents a collection of a chart cells."""



    @property
    def data_source_type(self) -> DataSourceType:
        ...

    @data_source_type.setter
    def data_source_type(self, value: DataSourceType):
        ...

    @property
    def data(self) -> object:
        ...

    @data.setter
    def data(self, value: object):
        ...

