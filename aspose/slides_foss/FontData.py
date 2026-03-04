from __future__ import annotations
from .IFontData import IFontData

class FontData(IFontData):
    """Represents a font definition. Immutable."""
    def __init__(self, font_name):
        self._font_name = font_name

    @property
    def font_name(self) -> str:
        """Returns the font name. Read/write ."""
        return self._font_name

    def get_font_name(self, theme) -> str:
        return self._font_name

