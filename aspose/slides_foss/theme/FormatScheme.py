from __future__ import annotations
from typing import TYPE_CHECKING
from .IFormatScheme import IFormatScheme
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from .IEffectStyleCollection import IEffectStyleCollection
    from .IFillFormatCollection import IFillFormatCollection
    from .ILineFormatCollection import ILineFormatCollection
    from ..IPresentation import IPresentation
    from .._internal.pptx.theme_part import ThemePart


class FormatScheme(IFormatScheme, ISlideComponent, IPresentationComponent):
    """Stores theme-defined formats for the shapes."""

    def _init_internal(self, fmt_scheme_elem, theme_part: ThemePart, presentation) -> None:
        self._fmt_scheme_elem = fmt_scheme_elem
        self._theme_part = theme_part
        self._presentation_ref = presentation
        self._fill_styles_cache = None
        self._line_styles_cache = None
        self._effect_styles_cache = None
        self._bg_fill_styles_cache = None

    @property
    def fill_styles(self) -> IFillFormatCollection:
        """Returns a collection of theme defined fill styles. Read-only ."""
        if self._fill_styles_cache is None:
            elem = self._fmt_scheme_elem.find(f"{NS.A}fillStyleLst")
            if elem is not None:
                from .FillFormatCollection import FillFormatCollection
                c = FillFormatCollection()
                c._init_internal(elem, self._theme_part)
                self._fill_styles_cache = c
        return self._fill_styles_cache

    @property
    def line_styles(self) -> ILineFormatCollection:
        """Returns a collection of theme defined line styles. Read-only ."""
        if self._line_styles_cache is None:
            elem = self._fmt_scheme_elem.find(f"{NS.A}lnStyleLst")
            if elem is not None:
                from .LineFormatCollection import LineFormatCollection
                c = LineFormatCollection()
                c._init_internal(elem, self._theme_part)
                self._line_styles_cache = c
        return self._line_styles_cache

    @property
    def effect_styles(self) -> IEffectStyleCollection:
        """Returns a collection of theme defined effect styles. Read-only ."""
        if self._effect_styles_cache is None:
            elem = self._fmt_scheme_elem.find(f"{NS.A}effectStyleLst")
            if elem is not None:
                from .EffectStyleCollection import EffectStyleCollection
                c = EffectStyleCollection()
                c._init_internal(elem, self._theme_part)
                self._effect_styles_cache = c
        return self._effect_styles_cache

    @property
    def background_fill_styles(self) -> IFillFormatCollection:
        """Returns a collection of theme defined background fill styles. Read-only ."""
        if self._bg_fill_styles_cache is None:
            elem = self._fmt_scheme_elem.find(f"{NS.A}bgFillStyleLst")
            if elem is not None:
                from .FillFormatCollection import FillFormatCollection
                c = FillFormatCollection()
                c._init_internal(elem, self._theme_part)
                self._bg_fill_styles_cache = c
        return self._bg_fill_styles_cache

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide. Read-only ."""
        return None

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation. Read-only ."""
        return self._presentation_ref

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self
