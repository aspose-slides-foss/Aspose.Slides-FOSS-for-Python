from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IChartWall import IChartWall

if TYPE_CHECKING:
    from .Format import Format
    from .._internal.pptx.chart_part import ChartPart
    from .IFormat import IFormat


class ChartWall(IChartWall):
    """Represents walls on 3D charts."""

    @property
    def thickness(self) -> int:
        from .._internal.pptx.constants import NS
        elem = self._wall_element.find(f'{NS.C}thickness')
        return int(elem.get('val', '0')) if elem is not None else 0

    @thickness.setter
    def thickness(self, value: int):
        from .._internal.pptx.constants import NS
        elem = self._wall_element.find(f'{NS.C}thickness')
        if elem is None:
            elem = ET.SubElement(self._wall_element, f'{NS.C}thickness')
        elem.set('val', str(value))

    @property
    def format(self) -> 'IFormat':
        from .Format import Format
        f = Format()
        f._init_internal(self._wall_element, self._chart_part)
        return f

    def _init_internal(self, wall_element, chart_part: 'ChartPart'):
        self._wall_element = wall_element
        self._chart_part = chart_part
        # Ensure <c:thickness val="0"/> exists (PowerPoint always writes it)
        from .._internal.pptx.constants import NS
        if wall_element.find(f'{NS.C}thickness') is None:
            thick = ET.Element(f'{NS.C}thickness')
            thick.set('val', '0')
            wall_element.insert(0, thick)
