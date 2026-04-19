from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IMultipleCellChartValue import IMultipleCellChartValue

if TYPE_CHECKING:
    from .IBaseChartValue import IBaseChartValue
    from .DataSourceType import DataSourceType
    from .IChartCellCollection import IChartCellCollection

class IStringChartValue(IMultipleCellChartValue, ABC):
    """Represent string value which can be stored in pptx presentation document in two ways: 1) in cell/cells of workbook related to chart; 2) as literal value."""
    @property
    def as_literal_string(self) -> str:
        """Returns or sets the literal string if DataSourceType property is DataSourceType.StringLiterals. Read/write ."""
        ...

    @as_literal_string.setter
    def as_literal_string(self, value: str):
        ...

    def to_string(self) -> str:
        ...

    def set_from_one_cell(self, cell) -> None:
        ...
