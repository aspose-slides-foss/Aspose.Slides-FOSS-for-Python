from __future__ import annotations
from typing import TYPE_CHECKING
from .Theme import Theme
from .IOverrideTheme import IOverrideTheme

if TYPE_CHECKING:
    from .ITheme import ITheme
    from ..IPresentationComponent import IPresentationComponent
    from .IColorScheme import IColorScheme
    from .IFontScheme import IFontScheme
    from .IFormatScheme import IFormatScheme
    from ..IPresentation import IPresentation


class OverrideTheme(Theme, IOverrideTheme):
    """Represents a overriding theme."""

    def _init_internal(self) -> None:
        self._color_scheme_obj = None
        self._font_scheme_obj = None
        self._format_scheme_obj = None

    @property
    def color_scheme(self) -> IColorScheme:
        """Returns the color scheme. Read-only ."""
        return self._color_scheme_obj

    @property
    def font_scheme(self) -> IFontScheme:
        """Returns the font scheme. Read-only ."""
        return self._font_scheme_obj

    @property
    def format_scheme(self) -> IFormatScheme:
        """Returns the shape format scheme. Read-only ."""
        return self._format_scheme_obj

    @property
    def presentation(self) -> IPresentation:
        return None

    @property
    def is_empty(self) -> bool:
        """True value means that ColorScheme, FontScheme, FormatScheme is null and any overriding with this theme object are disabled. Read-only ."""
        return (self._color_scheme_obj is None and
                self._font_scheme_obj is None and
                self._format_scheme_obj is None)

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def as_i_theme(self) -> ITheme:
        return self

    def clear(self) -> None:
        self._color_scheme_obj = None
        self._font_scheme_obj = None
        self._format_scheme_obj = None
