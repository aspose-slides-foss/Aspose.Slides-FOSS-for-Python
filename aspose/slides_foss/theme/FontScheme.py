from __future__ import annotations
from typing import TYPE_CHECKING
from .IFontScheme import IFontScheme
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from ..IFonts import IFonts
    from .._internal.pptx.theme_part import ThemePart

class FontScheme(IFontScheme):
    """Stores theme-defined fonts."""

    def _init_internal(self, font_scheme_elem, theme_part: ThemePart) -> None:
        self._font_scheme_elem = font_scheme_elem
        self._theme_part = theme_part
        self._major_cache = None
        self._minor_cache = None

    @property
    def minor(self) -> IFonts:
        """Returns the fonts collection for a "body" part of the slide. Read-only ."""
        if self._minor_cache is None:
            elem = self._font_scheme_elem.find(f"{NS.A}minorFont")
            if elem is not None:
                from ..Fonts import Fonts
                f = Fonts()
                f._init_internal(elem, self._theme_part)
                self._minor_cache = f
        return self._minor_cache

    @property
    def major(self) -> IFonts:
        """Returns the fonts collection for a "heading" part of the slide. Read-only ."""
        if self._major_cache is None:
            elem = self._font_scheme_elem.find(f"{NS.A}majorFont")
            if elem is not None:
                from ..Fonts import Fonts
                f = Fonts()
                f._init_internal(elem, self._theme_part)
                self._major_cache = f
        return self._major_cache

    @property
    def name(self) -> str:
        """Returns the font scheme name. Read/write ."""
        return self._font_scheme_elem.get('name', '')

    @name.setter
    def name(self, value: str):
        self._font_scheme_elem.set('name', value)
        self._theme_part.save()
