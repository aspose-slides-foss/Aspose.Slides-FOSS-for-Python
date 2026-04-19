from __future__ import annotations
from typing import TYPE_CHECKING
from .IExtraColorScheme import IExtraColorScheme
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from .IColorScheme import IColorScheme
    from .._internal.pptx.theme_part import ThemePart


class ExtraColorScheme(IExtraColorScheme):
    """Represents an additional color scheme which can be assigned to a slide."""

    def _init_internal(self, extra_elem, theme_part: ThemePart, presentation) -> None:
        self._extra_elem = extra_elem
        self._theme_part = theme_part
        self._presentation_ref = presentation
        self._color_scheme_cache = None

    @property
    def name(self) -> str:
        """Returns a name of this scheme. Read-only ."""
        clr_scheme = self._extra_elem.find(f"{NS.A}clrScheme")
        if clr_scheme is not None:
            return clr_scheme.get('name', '')
        return ''

    @property
    def color_scheme(self) -> IColorScheme:
        """Returns a color scheme. Read-only ."""
        if self._color_scheme_cache is None:
            clr_scheme = self._extra_elem.find(f"{NS.A}clrScheme")
            if clr_scheme is not None:
                from .ColorScheme import ColorScheme
                cs = ColorScheme()
                cs._init_internal(clr_scheme, self._theme_part, self._presentation_ref)
                self._color_scheme_cache = cs
        return self._color_scheme_cache
