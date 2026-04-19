from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IChartTextFormat import IChartTextFormat

if TYPE_CHECKING:
    from .ChartPortionFormat import ChartPortionFormat
    from .IChartPortionFormat import IChartPortionFormat


class ChartTextFormat(IChartTextFormat):
    """Specifies default text formatting for chart text elements."""

    @property
    def portion_format(self) -> IChartPortionFormat:
        from .ChartPortionFormat import ChartPortionFormat
        defRPr = self._get_or_create_defRPr()
        cpf = ChartPortionFormat()
        cpf._init_internal(defRPr, self._chart_part, None)
        return cpf

    def _get_or_create_txPr(self):
        from .._internal.pptx.constants import NS
        A = NS.A
        C = NS.C
        txPr = self._parent_element.find(f'{C}txPr')
        if txPr is None:
            txPr = ET.SubElement(self._parent_element, f'{C}txPr')
            ET.SubElement(txPr, f'{A}bodyPr')
            ET.SubElement(txPr, f'{A}lstStyle')
            p = ET.SubElement(txPr, f'{A}p')
            pPr = ET.SubElement(p, f'{A}pPr')
            ET.SubElement(pPr, f'{A}defRPr')
        return txPr

    def _get_or_create_defRPr(self):
        from .._internal.pptx.constants import NS
        A = NS.A
        txPr = self._get_or_create_txPr()
        p = txPr.find(f'{A}p')
        if p is None:
            p = ET.SubElement(txPr, f'{A}p')
        pPr = p.find(f'{A}pPr')
        if pPr is None:
            pPr = ET.SubElement(p, f'{A}pPr')
        defRPr = pPr.find(f'{A}defRPr')
        if defRPr is None:
            defRPr = ET.SubElement(pPr, f'{A}defRPr')
        return defRPr

    def _init_internal(self, parent_element, chart_part):
        self._parent_element = parent_element
        self._chart_part = chart_part
