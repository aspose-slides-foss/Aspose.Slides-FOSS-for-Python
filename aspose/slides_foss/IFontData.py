from __future__ import annotations
from abc import ABC, abstractmethod

class IFontData(ABC):
    """Represents a font definition."""
    @property
    def font_name(self) -> str:
        """Returns the font name. Read-only ."""
        ...
    def get_font_name(self, theme) -> str:
        ...

