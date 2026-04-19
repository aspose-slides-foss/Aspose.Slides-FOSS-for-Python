from __future__ import annotations
from typing import TYPE_CHECKING
from .Theme import Theme
from .IMasterTheme import IMasterTheme

if TYPE_CHECKING:
    from .ITheme import ITheme
    from ..IPresentationComponent import IPresentationComponent
    from .IExtraColorSchemeCollection import IExtraColorSchemeCollection
    from .._internal.pptx.theme_part import ThemePart


class MasterTheme(Theme, IMasterTheme):
    """Represents a master theme."""

    def _init_internal(self, theme_part: ThemePart, presentation) -> None:
        super()._init_internal(theme_part, presentation)
        self._extra_color_schemes_cache = None

    @property
    def extra_color_schemes(self) -> IExtraColorSchemeCollection:
        """Returns the collection of additional color schemes. Read-only ."""
        if self._extra_color_schemes_cache is None:
            elem = self._theme_part.extra_color_schemes_element
            from .ExtraColorSchemeCollection import ExtraColorSchemeCollection
            c = ExtraColorSchemeCollection()
            c._init_internal(elem, self._theme_part, self._presentation_ref)
            self._extra_color_schemes_cache = c
        return self._extra_color_schemes_cache

    @property
    def name(self) -> str:
        """Returns the name of a theme. Read/write ."""
        return self._theme_part.name

    @name.setter
    def name(self, value: str):
        self._theme_part.name = value
        self._theme_part.save()

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def as_i_theme(self) -> ITheme:
        return self
