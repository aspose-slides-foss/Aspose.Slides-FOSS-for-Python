from __future__ import annotations
from typing import TYPE_CHECKING
from .IFonts import IFonts
from ._internal.pptx.constants import NS

if TYPE_CHECKING:
    from .IFontData import IFontData
    from ._internal.pptx.theme_part import ThemePart

import lxml.etree as ET


class Fonts(IFonts):
    """Fonts collection."""

    def _init_internal(self, font_elem: ET._Element, theme_part: ThemePart) -> None:
        """
        Internal initialization.

        Args:
            font_elem: The <a:majorFont> or <a:minorFont> XML element.
            theme_part: The theme part for saving changes.
        """
        self._font_elem = font_elem
        self._theme_part = theme_part

    def _get_font_data(self, tag: str) -> IFontData:
        elem = self._font_elem.find(f"{NS.A}{tag}")
        if elem is not None:
            typeface = elem.get('typeface', '')
            from .FontData import FontData
            return FontData(typeface)
        return None

    def _set_font_data(self, tag: str, value: IFontData) -> None:
        elem = self._font_elem.find(f"{NS.A}{tag}")
        if elem is None:
            elem = ET.SubElement(self._font_elem, f"{NS.A}{tag}")
        elem.set('typeface', value.font_name if value else '')
        # Remove panose attribute when changing font — it's font-specific metadata
        if 'panose' in elem.attrib:
            del elem.attrib['panose']
        self._theme_part.save()

    @property
    def latin_font(self) -> IFontData:
        """Returns or sets the Latin font. Read/write ."""
        return self._get_font_data('latin')

    @latin_font.setter
    def latin_font(self, value: IFontData):
        self._set_font_data('latin', value)

    @property
    def east_asian_font(self) -> IFontData:
        """Returns or sets the East Asian font. Read/write ."""
        return self._get_font_data('ea')

    @east_asian_font.setter
    def east_asian_font(self, value: IFontData):
        self._set_font_data('ea', value)

    @property
    def complex_script_font(self) -> IFontData:
        """Returns or sets the complex script font. Read/write ."""
        return self._get_font_data('cs')

    @complex_script_font.setter
    def complex_script_font(self, value: IFontData):
        self._set_font_data('cs', value)
