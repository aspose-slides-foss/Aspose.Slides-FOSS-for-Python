from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBaseChartValue import IBaseChartValue

if TYPE_CHECKING:
    from .DataSourceType import DataSourceType
    from .IChartDataCell import IChartDataCell

class ISingleCellChartValue(IBaseChartValue, ABC):
    """Represents a chart data cell."""
    @property
    def as_cell(self) -> IChartDataCell:
        """Returns or sets chart data cell. Read/write ."""
        ...

    @as_cell.setter
    def as_cell(self, value: IChartDataCell):
        ...


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

