from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..IEffectFormat import IEffectFormat
    from ..ILineFormat import ILineFormat

class IChartLinesFormat(ABC):
    """Represents gridlines format properties."""
    @property
    def line(self) -> ILineFormat:
        """Returns line style properties of a chart line. Read-only ."""
        ...

    @property
    def effect(self) -> IEffectFormat:
        """Returns effects used for a chart line. Read-only ."""
        ...
