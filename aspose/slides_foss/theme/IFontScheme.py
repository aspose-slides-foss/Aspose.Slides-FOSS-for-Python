from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..IFonts import IFonts

class IFontScheme(ABC):
    """Stores theme-defined fonts."""
    @property
    @abstractmethod
    def minor(self) -> IFonts:
        """Returns the fonts collection for a "body" part of the slide. Read-only ."""
        ...

    @property
    @abstractmethod
    def major(self) -> IFonts:
        """Returns the fonts collection for a "heading" part of the slide. Read-only ."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the font scheme name. Read/write ."""
        ...

    @name.setter
    @abstractmethod
    def name(self, value: str):
        ...

