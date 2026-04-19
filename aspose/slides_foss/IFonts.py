from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFontData import IFontData

class IFonts(ABC):
    """Represents fonts collection."""
    @property
    @abstractmethod
    def latin_font(self) -> IFontData:
        """Returns or sets the Latin font. Read/write ."""
        ...

    @latin_font.setter
    @abstractmethod
    def latin_font(self, value: IFontData):
        ...

    @property
    @abstractmethod
    def east_asian_font(self) -> IFontData:
        """Returns or sets the East Asian font. Read/write ."""
        ...

    @east_asian_font.setter
    @abstractmethod
    def east_asian_font(self, value: IFontData):
        ...

    @property
    @abstractmethod
    def complex_script_font(self) -> IFontData:
        """Returns or sets the complex script font. Read/write ."""
        ...

    @complex_script_font.setter
    @abstractmethod
    def complex_script_font(self, value: IFontData):
        ...

