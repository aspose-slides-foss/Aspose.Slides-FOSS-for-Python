from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IChartParagraphFormat import IChartParagraphFormat
    from .IChartPortionFormat import IChartPortionFormat
    from .IChartTextBlockFormat import IChartTextBlockFormat

class IChartTextFormat(ABC):
    """Chart operate with restricted set of text format properties. IChartTextFormat, IChartTextBlockFormat, IChartParagraphFormat, IChartPortionFormat interfaces describe this restricted set."""
    @property
    def portion_format(self) -> IChartPortionFormat:
        """Returns portion format. Read-only ."""
        ...
