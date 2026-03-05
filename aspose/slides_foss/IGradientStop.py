from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat

class IGradientStop(ABC):
    """Represents a gradient format."""
    @property
    def position(self) -> float:
        """Returns or sets the position (0..1) of a gradient stop. Read/write ."""
        ...

    @position.setter
    def position(self, value: float):
        ...

    @property
    def color(self) -> IColorFormat:
        """Returns the color of a gradient stop. Read-only ."""
        ...

