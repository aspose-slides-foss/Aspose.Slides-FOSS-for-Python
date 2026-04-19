from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IFormat import IFormat

if TYPE_CHECKING:
    from ..IFillFormat import IFillFormat
    from ..ILineFormat import ILineFormat
    from ..IEffectFormat import IEffectFormat
    from ..IThreeDFormat import IThreeDFormat


class Format(IFormat):
    """Represents chart format properties (fill, line, effect, 3D)."""

    @property
    def fill(self) -> IFillFormat:
        from ..FillFormat import FillFormat
        spPr = self._get_or_create_spPr()
        ff = FillFormat()
        ff._init_internal(spPr, self._chart_part, None)
        return ff

    @property
    def line(self) -> ILineFormat:
        from ..LineFormat import LineFormat
        spPr = self._get_or_create_spPr()
        lf = LineFormat()
        lf._init_internal(spPr, self._chart_part, None)
        return lf

    @property
    def effect(self) -> IEffectFormat:
        from ..EffectFormat import EffectFormat
        spPr = self._get_or_create_spPr()
        ef = EffectFormat()
        ef._init_internal(spPr, self._chart_part, None)
        return ef

    @property
    def effect_3d(self) -> IThreeDFormat:
        from ..ThreeDFormat import ThreeDFormat
        spPr = self._get_or_create_spPr()
        td = ThreeDFormat()
        td._init_internal(spPr, self._chart_part, None)
        return td

    def _get_or_create_spPr(self):
        from .._internal.pptx.constants import NS
        spPr = self._parent_element.find(f'{NS.C}spPr')
        if spPr is None:
            spPr = ET.SubElement(self._parent_element, f'{NS.C}spPr')
        return spPr

    def _init_internal(self, parent_element, chart_part):
        self._parent_element = parent_element
        self._chart_part = chart_part
