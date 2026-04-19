from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IChartLinesFormat import IChartLinesFormat

if TYPE_CHECKING:
    from ..ILineFormat import ILineFormat
    from ..IEffectFormat import IEffectFormat


class ChartLinesFormat(IChartLinesFormat):
    """Represents gridlines format properties."""

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

    def _get_or_create_spPr(self):
        from .._internal.pptx.constants import NS
        spPr = self._gridlines_element.find(f'{NS.C}spPr')
        if spPr is None:
            spPr = ET.SubElement(self._gridlines_element, f'{NS.C}spPr')
        return spPr

    def _init_internal(self, gridlines_element, chart_part):
        self._gridlines_element = gridlines_element
        self._chart_part = chart_part
