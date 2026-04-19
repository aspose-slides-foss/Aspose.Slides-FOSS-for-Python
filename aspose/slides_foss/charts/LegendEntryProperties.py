from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ILegendEntryProperties import ILegendEntryProperties

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .ChartTextFormat import ChartTextFormat
    from .IChartTextFormat import IChartTextFormat


class LegendEntryProperties(ILegendEntryProperties):
    """Represents legend properties of a chart entry.

    Each entry corresponds to a series (by index).  The OOXML element is
    ``<c:legendEntry>`` with a child ``<c:idx val="N"/>``.  Optionally it
    contains ``<c:delete val="1"/>`` (hidden) and/or ``<c:txPr>`` for
    per-entry text formatting.
    """

    def _init_internal(self, index: int, legend_elem, chart_part: 'ChartPart'):
        """
        Args:
            index: 0-based series index this entry represents.
            legend_elem: The parent ``<c:legend>`` element.
            chart_part: The owning ChartPart (for save).
        """
        self._index = index
        self._legend_elem = legend_elem
        self._chart_part = chart_part
        return self

    # ------------------------------------------------------------------ #
    #  hide
    # ------------------------------------------------------------------ #

    @property
    def hide(self) -> bool:
        """Determines whether the legend entry is hidden. Read/write."""
        entry = self._find_entry_elem()
        if entry is None:
            return False
        from .._internal.pptx.constants import NS
        delete = entry.find(f'{NS.C}delete')
        if delete is not None:
            return delete.get('val', '0') == '1'
        return False

    @hide.setter
    def hide(self, value: bool):
        from .._internal.pptx.constants import NS
        entry = self._ensure_entry_elem()
        delete = entry.find(f'{NS.C}delete')
        if value:
            if delete is None:
                delete = ET.SubElement(entry, f'{NS.C}delete')
            delete.set('val', '1')
        else:
            if delete is not None:
                entry.remove(delete)
            # If entry is now empty (only idx child), remove it entirely
            if len(entry) == 1:  # just <c:idx>
                self._legend_elem.remove(entry)
        self._chart_part.save()

    # ------------------------------------------------------------------ #
    #  text_format
    # ------------------------------------------------------------------ #

    @property
    def text_format(self) -> 'IChartTextFormat':
        """Returns text format for this legend entry. Read-only."""
        from .ChartTextFormat import ChartTextFormat
        entry = self._ensure_entry_elem()
        ctf = ChartTextFormat()
        ctf._init_internal(entry, self._chart_part)
        return ctf

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _find_entry_elem(self):
        """Find existing <c:legendEntry> for this index, or None."""
        from .._internal.pptx.constants import NS
        if self._legend_elem is None:
            return None
        for le in self._legend_elem.findall(f'{NS.C}legendEntry'):
            idx_elem = le.find(f'{NS.C}idx')
            if idx_elem is not None and idx_elem.get('val') == str(self._index):
                return le
        return None

    def _ensure_entry_elem(self):
        """Get or create the <c:legendEntry> for this index.

        Inserts after legendPos/other legendEntry elements but before
        layout/overlay/spPr/txPr to respect OOXML element ordering.
        """
        entry = self._find_entry_elem()
        if entry is not None:
            return entry
        from .._internal.pptx.constants import NS
        entry = ET.Element(f'{NS.C}legendEntry')
        idx_elem = ET.SubElement(entry, f'{NS.C}idx')
        idx_elem.set('val', str(self._index))
        # Find insertion point: after legendPos and other legendEntry elements
        _LATER = {'layout', 'overlay', 'spPr', 'txPr', 'extLst'}
        insert_at = len(self._legend_elem)
        for i, child in enumerate(self._legend_elem):
            local = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
            if local in _LATER:
                insert_at = i
                break
        self._legend_elem.insert(insert_at, entry)
        return entry
