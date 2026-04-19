from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IChartTitle import IChartTitle

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from ..ITextFrame import ITextFrame


class ChartTitle(IChartTitle):
    """Represents chart title properties."""

    def _init_internal(self, title_elem, chart_part: 'ChartPart', parent_element):
        """Initialize from a <c:title> XML element.

        Args:
            title_elem: The <c:title> element (may be None if title not yet created).
            chart_part: The owning ChartPart.
            parent_element: The parent XML element (<c:chart> or axis element)
                            where <c:title> lives.
        """
        self._title_elem = title_elem
        self._chart_part = chart_part
        self._parent_element = parent_element
        self._text_frame = None
        return self

    # ------------------------------------------------------------------ #
    #  overlay
    # ------------------------------------------------------------------ #

    @property
    def overlay(self) -> bool:
        from .._internal.pptx.constants import NS
        if self._title_elem is None:
            return False
        ov = self._title_elem.find(f'{NS.C}overlay')
        if ov is not None:
            return ov.get('val', '0') == '1'
        return False

    @overlay.setter
    def overlay(self, value: bool):
        from .._internal.pptx.constants import NS
        self._ensure_title_elem()
        ov = self._title_elem.find(f'{NS.C}overlay')
        if ov is None:
            ov = ET.SubElement(self._title_elem, f'{NS.C}overlay')
        ov.set('val', '1' if value else '0')
        self._chart_part.save()

    # ------------------------------------------------------------------ #
    #  text_frame_for_overriding
    # ------------------------------------------------------------------ #

    @property
    def text_frame_for_overriding(self) -> 'ITextFrame':
        """Returns the overriding text frame, or None if not set."""
        from .._internal.pptx.constants import NS
        if self._title_elem is None:
            return None
        tx = self._title_elem.find(f'{NS.C}tx')
        if tx is None:
            return None
        rich = tx.find(f'{NS.C}rich')
        if rich is None:
            return None
        # Build a TextFrame wrapping <c:rich> (same children as <a:txBody>)
        from ..TextFrame import TextFrame
        tf = TextFrame()
        tf._init_internal(rich, self._chart_part, None)
        return tf

    # ------------------------------------------------------------------ #
    #  add_text_frame_for_overriding
    # ------------------------------------------------------------------ #

    def add_text_frame_for_overriding(self, text) -> 'ITextFrame':
        """Create or replace the overriding text frame with initial text."""
        from .._internal.pptx.constants import NS

        self._ensure_title_elem()

        # Remove existing <c:tx> if any
        tx = self._title_elem.find(f'{NS.C}tx')
        if tx is not None:
            self._title_elem.remove(tx)

        # Build <c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p>...</a:p></c:rich></c:tx>
        tx = ET.SubElement(self._title_elem, f'{NS.C}tx')
        rich = ET.SubElement(tx, f'{NS.C}rich')
        ET.SubElement(rich, f'{NS.A}bodyPr')
        ET.SubElement(rich, f'{NS.A}lstStyle')

        p = ET.SubElement(rich, f'{NS.A}p')
        p_pr = ET.SubElement(p, f'{NS.A}pPr')
        ET.SubElement(p_pr, f'{NS.A}defRPr')

        r = ET.SubElement(p, f'{NS.A}r')
        t = ET.SubElement(r, f'{NS.A}t')
        t.text = text if text else ''

        # Ensure overlay element exists (default to val="1" per OOXML conventions)
        ov = self._title_elem.find(f'{NS.C}overlay')
        if ov is None:
            ov = ET.SubElement(self._title_elem, f'{NS.C}overlay')
            ov.set('val', '1')

        self._chart_part.save()

        # Return a TextFrame wrapping the <c:rich> element
        from ..TextFrame import TextFrame
        tf = TextFrame()
        tf._init_internal(rich, self._chart_part, None)
        return tf

    # ------------------------------------------------------------------ #
    #  text_format
    # ------------------------------------------------------------------ #

    @property
    def text_format(self):
        from .ChartTextFormat import ChartTextFormat
        if self._title_elem is None:
            return None
        ctf = ChartTextFormat()
        ctf._init_internal(self._title_elem, self._chart_part)
        return ctf

    # ------------------------------------------------------------------ #
    #  format (fill/line/effect)
    # ------------------------------------------------------------------ #

    @property
    def format(self):
        from .Format import Format
        if self._title_elem is None:
            return None
        fmt = Format()
        fmt._init_internal(self._title_elem, self._chart_part)
        return fmt

    # ------------------------------------------------------------------ #
    #  layout properties (x, y, width, height)
    # ------------------------------------------------------------------ #

    @property
    def x(self) -> float:
        return self._read_layout_val('x')

    @x.setter
    def x(self, value: float):
        self._write_layout_val('x', value)

    @property
    def y(self) -> float:
        return self._read_layout_val('y')

    @y.setter
    def y(self, value: float):
        self._write_layout_val('y', value)

    @property
    def width(self) -> float:
        return self._read_layout_val('w')

    @width.setter
    def width(self, value: float):
        self._write_layout_val('w', value)

    @property
    def height(self) -> float:
        return self._read_layout_val('h')

    @height.setter
    def height(self, value: float):
        self._write_layout_val('h', value)

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _ensure_title_elem(self):
        """Create <c:title> under the parent if it doesn't exist.

        Inserted at the schema-correct position (before autoTitleDeleted /
        plotArea / legend etc.) so that the resulting chart XML passes the
        OOXML sequence constraint for <c:chart> children.
        """
        if self._title_elem is not None:
            return
        from .._internal.pptx.constants import NS
        from .Chart import Chart
        self._title_elem = ET.Element(f'{NS.C}title')
        order = Chart._CHART_CHILD_ORDER
        target_idx = order.index('title')
        insert_pos = len(self._parent_element)
        for i, child in enumerate(self._parent_element):
            child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if child_local in order and order.index(child_local) >= target_idx:
                insert_pos = i
                break
        self._parent_element.insert(insert_pos, self._title_elem)

    def _read_layout_val(self, attr: str) -> float:
        """Read a manual layout value from <c:layout><c:manualLayout>."""
        from .._internal.pptx.constants import NS
        if self._title_elem is None:
            return 0.0
        layout = self._title_elem.find(f'{NS.C}layout')
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
        """Write a manual layout value."""
        from .._internal.pptx.constants import NS
        self._ensure_title_elem()
        layout = self._title_elem.find(f'{NS.C}layout')
        if layout is None:
            layout = ET.SubElement(self._title_elem, f'{NS.C}layout')
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            ml = ET.SubElement(layout, f'{NS.C}manualLayout')
            # Add xMode/yMode=edge (required by OOXML for manual layout)
            x_mode = ET.SubElement(ml, f'{NS.C}xMode')
            x_mode.set('val', 'edge')
            y_mode = ET.SubElement(ml, f'{NS.C}yMode')
            y_mode.set('val', 'edge')
        elem = ml.find(f'{NS.C}{attr}')
        if elem is None:
            elem = ET.SubElement(ml, f'{NS.C}{attr}')
        elem.set('val', str(value))
        self._chart_part.save()
