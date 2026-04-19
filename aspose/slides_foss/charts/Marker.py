from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from .MarkerStyleType import MarkerStyleType
from .IMarker import IMarker

if TYPE_CHECKING:
    from .ChartSeries import ChartSeries
    from .Format import Format
    from .._internal.pptx.chart_part import ChartPart
    from .IFormat import IFormat


# Child order inside <c:marker> (CT_Marker).
_MARKER_ORDER = ('symbol', 'size', 'spPr', 'extLst')

# Child order inside <c:dPt> (CT_DPt) — the per-data-point container.
_DPT_ORDER = (
    'idx', 'invertIfNegative', 'marker', 'bubble3D',
    'explosion', 'spPr', 'pictureOptions', 'extLst',
)


_SYMBOL_TO_XML = {
    MarkerStyleType.CIRCLE: 'circle',
    MarkerStyleType.DASH: 'dash',
    MarkerStyleType.DIAMOND: 'diamond',
    MarkerStyleType.DOT: 'dot',
    MarkerStyleType.NONE: 'none',
    MarkerStyleType.PICTURE: 'picture',
    MarkerStyleType.PLUS: 'plus',
    MarkerStyleType.SQUARE: 'square',
    MarkerStyleType.STAR: 'star',
    MarkerStyleType.TRIANGLE: 'triangle',
    MarkerStyleType.X: 'x',
}
_XML_TO_SYMBOL = {v: k for k, v in _SYMBOL_TO_XML.items()}


class Marker(IMarker):
    """Represents a chart marker (symbol at data points).

    Wraps a <c:marker> element. The element lives either directly inside
    <c:ser> (series-level, affecting all points) or inside <c:dPt>/<c:marker>
    (per-data-point override). Series-level storage is on
    ChartSeries._marker_elem; per-point is on ChartSeries._dpt_elems[index].
    """

    def _init_internal(self, series: 'ChartSeries',
                       chart_part: 'ChartPart',
                       point_index: int | None = None):
        from .._internal.pptx.constants import NS
        self._series = series
        self._chart_part = chart_part
        self._point_index = point_index
        self._ns_c = NS.C

    # ---- element access ----

    def _c(self, local: str) -> str:
        return f'{self._ns_c}{local}'

    def _find_elem(self):
        """Return the <c:marker> element, or None if not present."""
        if self._point_index is None:
            return getattr(self._series, '_marker_elem', None)
        dpt = getattr(self._series, '_dpt_elems', {}).get(self._point_index)
        if dpt is None:
            return None
        return dpt.find(self._c('marker'))

    def _ensure_elem(self):
        """Return the <c:marker>; create it (and parent <c:dPt>) if missing."""
        elem = self._find_elem()
        if elem is not None:
            return elem
        if self._point_index is None:
            elem = ET.Element(self._c('marker'))
            self._series._marker_elem = elem
            return elem
        # Per-point: ensure <c:dPt> exists in the series storage.
        dpt = self._series._dpt_elems.get(self._point_index)
        if dpt is None:
            dpt = ET.Element(self._c('dPt'))
            idx = ET.SubElement(dpt, self._c('idx'))
            idx.set('val', str(self._point_index))
            # invertIfNegative: always emit val="1" inside a per-point <c:dPt>
            # regardless of chart type. It is a no-op for marker-only overrides
            # (line/scatter/radar); this matches the default PowerPoint emits
            # and preserves round-trip XML parity.
            inv = ET.SubElement(dpt, self._c('invertIfNegative'))
            inv.set('val', '1')
            self._series._dpt_elems[self._point_index] = dpt
        elem = ET.Element(self._c('marker'))
        _insert_in_order(dpt, elem, 'marker', _DPT_ORDER, self._ns_c)
        return elem

    # ---- public properties ----

    @property
    def symbol(self) -> MarkerStyleType:
        elem = self._find_elem()
        if elem is None:
            return MarkerStyleType.NOT_DEFINED
        sym = elem.find(self._c('symbol'))
        if sym is None:
            return MarkerStyleType.NOT_DEFINED
        return _XML_TO_SYMBOL.get(sym.get('val', ''), MarkerStyleType.NOT_DEFINED)

    @symbol.setter
    def symbol(self, value: MarkerStyleType):
        if value == MarkerStyleType.NOT_DEFINED:
            elem = self._find_elem()
            if elem is None:
                return
            sym = elem.find(self._c('symbol'))
            if sym is not None:
                elem.remove(sym)
            return
        elem = self._ensure_elem()
        sym = elem.find(self._c('symbol'))
        if sym is None:
            sym = ET.Element(self._c('symbol'))
            _insert_in_order(elem, sym, 'symbol', _MARKER_ORDER, self._ns_c)
        sym.set('val', _SYMBOL_TO_XML[value])

    @property
    def size(self) -> int:
        elem = self._find_elem()
        if elem is None:
            return 0
        sz = elem.find(self._c('size'))
        if sz is None:
            return 0
        try:
            return int(sz.get('val', '0'))
        except ValueError:
            return 0

    @size.setter
    def size(self, value: int):
        elem = self._ensure_elem()
        sz = elem.find(self._c('size'))
        if sz is None:
            sz = ET.Element(self._c('size'))
            _insert_in_order(elem, sz, 'size', _MARKER_ORDER, self._ns_c)
        sz.set('val', str(int(value)))

    @property
    def format(self) -> 'IFormat':
        """Fill/line/effect format for the marker. Read-only."""
        from .Format import Format
        elem = self._ensure_elem()
        # Pre-create <c:spPr> in the correct ordinal position so that later
        # Format.fill / Format.line lookups find it without appending out-of-order.
        spPr = elem.find(self._c('spPr'))
        if spPr is None:
            spPr = ET.Element(self._c('spPr'))
            _insert_in_order(elem, spPr, 'spPr', _MARKER_ORDER, self._ns_c)
        fmt = Format()
        fmt._init_internal(elem, self._chart_part)
        return fmt


def _insert_in_order(parent, new_child, local_name: str,
                     order: tuple, ns: str) -> None:
    """Insert new_child into parent at the position implied by order list."""
    try:
        idx = order.index(local_name)
    except ValueError:
        parent.append(new_child)
        return
    later = {f'{ns}{t}' for t in order[idx + 1:]}
    insert_before = None
    for child in parent:
        if child.tag in later:
            insert_before = child
            break
    if insert_before is not None:
        parent.insert(list(parent).index(insert_before), new_child)
    else:
        parent.append(new_child)
