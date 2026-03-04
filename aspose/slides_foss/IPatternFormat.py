from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat
    from .IImage import IImage
    from .PatternStyle import PatternStyle

class IPatternFormat(ABC):
    """Represents a pattern to fill a shape."""
    @property
    def pattern_style(self) -> PatternStyle:
        """Returns or sets the pattern style. Read/write ."""
        ...

    @pattern_style.setter
    def pattern_style(self, value: PatternStyle):
        ...

    @property
    def fore_color(self) -> IColorFormat:
        """Returns the foreground pattern color. Read-only ."""
        ...

    @property
    def back_color(self) -> IColorFormat:
        """Returns the background pattern color. Read-only ."""
        ...




