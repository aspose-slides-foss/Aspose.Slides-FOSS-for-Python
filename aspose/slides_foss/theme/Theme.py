from __future__ import annotations
from typing import TYPE_CHECKING
from .ITheme import ITheme
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IColorScheme import IColorScheme
    from .IFontScheme import IFontScheme
    from .IFormatScheme import IFormatScheme
    from ..IPresentation import IPresentation
    from .._internal.pptx.theme_part import ThemePart


class Theme(ITheme, IPresentationComponent):
    """Represents a theme."""

    def _init_internal(self, theme_part: ThemePart, presentation) -> None:
        self._theme_part = theme_part
        self._presentation_ref = presentation
        self._color_scheme_cache = None
        self._font_scheme_cache = None
        self._format_scheme_cache = None

    @property
    def color_scheme(self) -> IColorScheme:
        """Returns the color scheme. Read-only ."""
        if self._color_scheme_cache is None:
            elem = self._theme_part.color_scheme_element
            if elem is not None:
                from .ColorScheme import ColorScheme
                cs = ColorScheme()
                cs._init_internal(elem, self._theme_part, self._presentation_ref)
                self._color_scheme_cache = cs
        return self._color_scheme_cache

    @property
    def font_scheme(self) -> IFontScheme:
        """Returns the font scheme. Read-only ."""
        if self._font_scheme_cache is None:
            elem = self._theme_part.font_scheme_element
            if elem is not None:
                from .FontScheme import FontScheme
                fs = FontScheme()
                fs._init_internal(elem, self._theme_part)
                self._font_scheme_cache = fs
        return self._font_scheme_cache

    @property
    def format_scheme(self) -> IFormatScheme:
        """Returns the shape format scheme. Read-only ."""
        if self._format_scheme_cache is None:
            elem = self._theme_part.format_scheme_element
            if elem is not None:
                from .FormatScheme import FormatScheme
                fms = FormatScheme()
                fms._init_internal(elem, self._theme_part, self._presentation_ref)
                self._format_scheme_cache = fms
        return self._format_scheme_cache

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation. Read-only ."""
        return self._presentation_ref

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self
