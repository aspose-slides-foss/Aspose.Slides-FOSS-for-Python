from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFormat import IFormat

class IUpDownBarsManager(ABC):
    """Provide access to up/down bars of Line- or Stock-chart."""




    @property
    def gap_width(self) -> int:
        """Returns or sets gap width. Read/write ."""
        ...

    @gap_width.setter
    def gap_width(self, value: int):
        ...

