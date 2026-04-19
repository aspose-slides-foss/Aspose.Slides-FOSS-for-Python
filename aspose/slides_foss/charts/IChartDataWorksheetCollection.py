from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IChartDataWorksheet import IChartDataWorksheet

class IChartDataWorksheetCollection(ABC):
    """Represents the collection of worksheets of chart data workbook."""

    def __getitem__(self, index: int) -> IChartDataWorksheet:
        ...

