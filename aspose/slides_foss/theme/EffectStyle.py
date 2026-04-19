from __future__ import annotations
from typing import TYPE_CHECKING
from .IEffectStyle import IEffectStyle
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from ..IEffectFormat import IEffectFormat
    from ..IThreeDFormat import IThreeDFormat
    from .._internal.pptx.theme_part import ThemePart

import lxml.etree as ET


class EffectStyle(IEffectStyle):
    """Represents an effect style."""

    def _init_internal(self, effect_style_elem: ET._Element, theme_part: ThemePart) -> None:
        self._effect_style_elem = effect_style_elem
        self._theme_part = theme_part
        self._effect_format_cache = None
        self._three_d_format_cache = None

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns an effect format. Read-only ."""
        if self._effect_format_cache is None:
            effect_lst = self._effect_style_elem.find(Elements.A_EFFECT_LST)
            if effect_lst is not None:
                from ..EffectFormat import EffectFormat
                ef = EffectFormat()
                ef._init_internal(self._effect_style_elem, self._theme_part, None)
                self._effect_format_cache = ef
        return self._effect_format_cache

    @property
    def three_d_format(self) -> IThreeDFormat:
        """Returns an 3d format. Read-only ."""
        if self._three_d_format_cache is None:
            sp3d = self._effect_style_elem.find(Elements.A_SP_3D)
            if sp3d is not None:
                from ..ThreeDFormat import ThreeDFormat
                td = ThreeDFormat()
                td._init_internal(self._effect_style_elem, self._theme_part, None)
                self._three_d_format_cache = td
        return self._three_d_format_cache
