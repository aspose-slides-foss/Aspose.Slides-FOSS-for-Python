from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ISingleCellChartValue import ISingleCellChartValue

if TYPE_CHECKING:
    from .IBaseChartValue import IBaseChartValue
    from .DataSourceType import DataSourceType
    from .IChartDataCell import IChartDataCell

class IStringOrDoubleChartValue(ISingleCellChartValue, ABC):
    """Represent string or double value which can be stored in pptx presentation document in two ways: 1) in cell/cells of workbook related to chart; 2) as literal value."""
    @property
    def as_literal_string(self) -> str:
        """Returns or sets the literal string if DataSourceType property is DataSourceType.StringLiterals. Read/write ."""
        ...

    @as_literal_string.setter
    def as_literal_string(self, value: str):
        ...

    @property
    def as_literal_double(self) -> float:
        """Returns or sets the literal double if DataSourceType property is DataSourceType.DoubleLiterals. Read/write ."""
        ...

    @as_literal_double.setter
    def as_literal_double(self, value: float):
        ...

    @property
    def as_cell(self) -> IChartDataCell:
        ...

    @as_cell.setter
    def as_cell(self, value: IChartDataCell):
        ...

    def to_double(self) -> float:
        ...
