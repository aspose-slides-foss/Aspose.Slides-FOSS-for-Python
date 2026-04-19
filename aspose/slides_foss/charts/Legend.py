from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ILegend import ILegend

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .IFormat import IFormat
    from .IChartTextFormat import IChartTextFormat
    from .ILegendEntryCollection import ILegendEntryCollection
    from .LegendPositionType import LegendPositionType

# OOXML legendPos val → LegendPositionType mapping
_POS_FROM_XML = {
    'b': 'BOTTOM',
    'l': 'LEFT',
    'r': 'RIGHT',
    't': 'TOP',
    'tr': 'TOP_RIGHT',
}
_POS_TO_XML = {v: k for k, v in _POS_FROM_XML.items()}


# OOXML CT_Legend child element order (strict sequence)
_LEGEND_CHILD_ORDER = [
    'legendPos',
    'legendEntry',
    'layout',
    'overlay',
    'spPr',
    'txPr',
    'extLst',
]


class Legend(ILegend):
    """Represents chart's legend properties."""

    def _init_internal(self, legend_elem, chart_part: 'ChartPart', chart_element, chart):
        """
        Args:
            legend_elem: The ``<c:legend>`` element (may be None).
            chart_part: The owning ChartPart.
            chart_element: The ``<c:chart>`` parent element.
            chart: The parent Chart object.
        """
        self._legend_elem = legend_elem
        self._chart_part = chart_part
        self._chart_element = chart_element
        self._chart = chart
        self._entries_cache = None
        return self

    # ------------------------------------------------------------------ #
    #  position
    # ------------------------------------------------------------------ #

    @property
    def position(self) -> LegendPositionType:
        """Specifies the position of the legend on a chart. Read/write."""
        from .LegendPositionType import LegendPositionType
        from .._internal.pptx.constants import NS
        if self._legend_elem is None:
            return LegendPositionType.BOTTOM
        lp = self._legend_elem.find(f'{NS.C}legendPos')
        if lp is not None:
            val = lp.get('val', 'b')
            name = _POS_FROM_XML.get(val, 'BOTTOM')
            return LegendPositionType[name]
        return LegendPositionType.BOTTOM

    @position.setter
    def position(self, value: LegendPositionType):
        from .._internal.pptx.constants import NS
        self._ensure_legend_elem()
        lp = self._legend_elem.find(f'{NS.C}legendPos')
        if lp is None:
            # Insert legendPos as first child
            lp = ET.Element(f'{NS.C}legendPos')
            self._legend_elem.insert(0, lp)
        xml_val = _POS_TO_XML.get(value.name, 'b')
        lp.set('val', xml_val)
        self._chart_part.save()

    # ------------------------------------------------------------------ #
    #  overlay
    # ------------------------------------------------------------------ #

    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap legend. Read/write."""
        from .._internal.pptx.constants import NS
        if self._legend_elem is None:
            return False
        ov = self._legend_elem.find(f'{NS.C}overlay')
        if ov is not None:
            return ov.get('val', '0') == '1'
        return False

    @overlay.setter
    def overlay(self, value: bool):
        from .._internal.pptx.constants import NS
        self._ensure_legend_elem()
        ov = self._legend_elem.find(f'{NS.C}overlay')
        if ov is None:
            ov = self._insert_child_ordered('overlay')
        ov.set('val', '1' if value else '0')
        self._chart_part.save()

    # ------------------------------------------------------------------ #
    #  format (fill / line / effect / 3D)
    # ------------------------------------------------------------------ #

    @property
    def format(self) -> IFormat:
        """Returns the format of a legend. Read-only."""
        from .Format import Format
        if self._legend_elem is None:
            return None
        fmt = Format()
        fmt._init_internal(self._legend_elem, self._chart_part)
        return fmt

    # ------------------------------------------------------------------ #
    #  text_format
    # ------------------------------------------------------------------ #

    @property
    def text_format(self) -> IChartTextFormat:
        """Text format. Read-only."""
        from .ChartTextFormat import ChartTextFormat
        if self._legend_elem is None:
            return None
        ctf = ChartTextFormat()
        ctf._init_internal(self._legend_elem, self._chart_part)
        return ctf

    # ------------------------------------------------------------------ #
    #  entries
    # ------------------------------------------------------------------ #

    @property
    def entries(self) -> ILegendEntryCollection:
        """Gets legend entries. Read-only."""
        if self._entries_cache is not None:
            return self._entries_cache
        from .LegendEntryCollection import LegendEntryCollection
        series_count = len(self._chart.chart_data.series) if self._chart is not None else 0
        coll = LegendEntryCollection()
        coll._init_internal(self._legend_elem, self._chart_part, series_count)
        self._entries_cache = coll
        return coll

    # ------------------------------------------------------------------ #
    #  layout properties (x, y, width, height)
    # ------------------------------------------------------------------ #

    @property
    def x(self) -> float:
        """X coordinate as a fraction of the chart width. Read/write."""
        return self._read_layout_val('x')

    @x.setter
    def x(self, value: float):
        self._write_layout_val('x', value)

    @property
    def y(self) -> float:
        """Y coordinate as a fraction of the chart height. Read/write."""
        return self._read_layout_val('y')

    @y.setter
    def y(self, value: float):
        self._write_layout_val('y', value)

    @property
    def width(self) -> float:
        """Width as a fraction of the chart width. Read/write."""
        return self._read_layout_val('w')

    @width.setter
    def width(self, value: float):
        self._write_layout_val('w', value)

    @property
    def height(self) -> float:
        """Height as a fraction of the chart height. Read/write."""
        return self._read_layout_val('h')

    @height.setter
    def height(self, value: float):
        self._write_layout_val('h', value)

    @property
    def right(self) -> float:
        """Right boundary. Read-only."""
        return self.x + self.width

    @property
    def bottom(self) -> float:
        """Bottom boundary. Read-only."""
        return self.y + self.height

    # ------------------------------------------------------------------ #
    #  chart reference
    # ------------------------------------------------------------------ #

    @property
    def chart(self):
        """Returns the parent chart. Read-only."""
        return self._chart

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _ensure_legend_elem(self):
        """Create <c:legend> under <c:chart> if it doesn't exist."""
        if self._legend_elem is not None:
            return
        from .._internal.pptx.constants import NS
        self._legend_elem = ET.SubElement(self._chart_element, f'{NS.C}legend')
        # Add default children in correct OOXML order
        lp = ET.SubElement(self._legend_elem, f'{NS.C}legendPos')
        lp.set('val', 'b')
        ov = ET.SubElement(self._legend_elem, f'{NS.C}overlay')
        ov.set('val', '0')

    def _insert_child_ordered(self, tag_local: str):
        """Create and insert a child element at the correct OOXML position.

        Returns the newly created element.
        """
        from .._internal.pptx.constants import NS
        target_idx = _LEGEND_CHILD_ORDER.index(tag_local)
        new_elem = ET.Element(f'{NS.C}{tag_local}')
        # Find the first existing child whose order index > target_idx
        for i, child in enumerate(self._legend_elem):
            child_local = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
            try:
                child_idx = _LEGEND_CHILD_ORDER.index(child_local)
            except ValueError:
                continue
            if child_idx > target_idx:
                self._legend_elem.insert(i, new_elem)
                return new_elem
        # Append at end if no later sibling found
        self._legend_elem.append(new_elem)
        return new_elem

    def _read_layout_val(self, attr: str) -> float:
        from .._internal.pptx.constants import NS
        if self._legend_elem is None:
            return 0.0
        layout = self._legend_elem.find(f'{NS.C}layout')
        if layout is None:
            return 0.0
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            return 0.0
        elem = ml.find(f'{NS.C}{attr}')
        if elem is not None:
            try:
                return float(elem.get('val', '0'))
            except ValueError:
                pass
        return 0.0

    def _write_layout_val(self, attr: str, value: float):
        from .._internal.pptx.constants import NS
        self._ensure_legend_elem()
        layout = self._legend_elem.find(f'{NS.C}layout')
        if layout is None:
            layout = self._insert_child_ordered('layout')
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            ml = ET.SubElement(layout, f'{NS.C}manualLayout')
            x_mode = ET.SubElement(ml, f'{NS.C}xMode')
            x_mode.set('val', 'edge')
            y_mode = ET.SubElement(ml, f'{NS.C}yMode')
            y_mode.set('val', 'edge')
        elem = ml.find(f'{NS.C}{attr}')
        if elem is None:
            elem = ET.SubElement(ml, f'{NS.C}{attr}')
        elem.set('val', str(value))
        self._chart_part.save()
