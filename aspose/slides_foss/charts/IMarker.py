from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFormat import IFormat
    from .MarkerStyleType import MarkerStyleType

class IMarker(ABC):
    """Represents marker of a chert."""
    @property
    def symbol(self) -> MarkerStyleType:
        """Represents the marker style in a line chart, scatter chart, or radar chart. Read/write ."""
        ...

    @symbol.setter
    def symbol(self, value: MarkerStyleType):
        ...

    @property
    def format(self) -> IFormat:
        """Gets the marker fill. Read-only ."""
        ...

    @property
    def size(self) -> int:
        """Represents the marker size in a line chart, scatter chart, or radar chart. Read/write ."""
        ...

    @size.setter
    def size(self, value: int):
        ...
