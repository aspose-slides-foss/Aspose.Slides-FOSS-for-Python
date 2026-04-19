from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from .DataLabelFormat import C15_NS, C15_EXT_URI
from .IDataLabel import IDataLabel

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from ..ITextFrame import ITextFrame
    from .ChartDataCell import ChartDataCell
    from .ChartTextFormat import ChartTextFormat
    from .DataLabelFormat import DataLabelFormat
    from .IChartDataCell import IChartDataCell
    from .IChartTextFormat import IChartTextFormat
    from .IDataLabelFormat import IDataLabelFormat


# Sibling order inside <c:dLbl> (strict OOXML order).
_DLBL_ORDER = (
    'idx', 'layout', 'tx', 'numFmt', 'spPr', 'txPr', 'dLblPos',
    'showLegendKey', 'showVal', 'showCatName', 'showSerName',
    'showPercent', 'showBubbleSize', 'separator',
    'showLeaderLines', 'extLst',
)


class DataLabel(IDataLabel):
    """Represents a series data point label.

    Wraps a <c:dLbl> element (per-data-point override) inside a <c:dLbls>
    collection.
    """

    def _init_internal(self, dlbl_elem, parent_collection, index: int,
                       chart_part: 'ChartPart'):
        from .._internal.pptx.constants import NS
        self._elem = dlbl_elem  # may be None until label written
        self._parent_collection = parent_collection
        self._index = index
        self._chart_part = chart_part
        self._ns_c = NS.C
        self._ns_a = NS.A

    # ---- element access helpers ----

    def _c(self, local: str) -> str:
        return f'{self._ns_c}{local}'

    def _ensure_dlbl(self):
        """Create the <c:dLbl> element inside parent <c:dLbls> if missing.

        New per-point labels inherit show_* flag values from the series
        default (the <c:dLbls> element), then PowerPoint treats the <c:dLbl>
        as a complete override and stops falling back to the series default.
        This matches commercial Aspose output and avoids PP corruption when
        a per-point override is written without an explicit show_* flag.
        """
        if self._elem is not None:
            return self._elem
        dlbls = self._parent_collection._ensure_dlbls()
        elem = _build_dlbl(self._index, self._ns_c)
        _seed_show_flags_from_defaults(elem, dlbls, self._ns_c)
        _insert_dlbl_sorted(dlbls, elem, self._index, self._ns_c)
        self._elem = elem
        return elem

    def _find(self, local: str):
        if self._elem is None:
            return None
        return self._elem.find(self._c(local))

    def _find_or_create(self, local: str):
        self._ensure_dlbl()
        e = self._elem.find(self._c(local))
        if e is None:
            e = ET.Element(self._c(local))
            _insert_sorted(self._elem, e, local, _DLBL_ORDER)
        return e

    # ---- basic properties ----

    @property
    def chart(self):
        return self._parent_collection.chart

    @property
    def slide(self):
        return self._parent_collection.slide

    @property
    def presentation(self):
        return self._parent_collection.presentation

    @property
    def is_visible(self) -> bool:
        """True when any show_* flag is set on this label or on the series default."""
        fmt = self.data_label_format
        if any([
            fmt.show_legend_key, fmt.show_value, fmt.show_category_name,
            fmt.show_series_name, fmt.show_percentage, fmt.show_bubble_size,
            fmt.show_label_value_from_cell,
        ]):
            return True
        # Fall back to series default
        default = self._parent_collection.default_data_label_format
        return any([
            default.show_legend_key, default.show_value, default.show_category_name,
            default.show_series_name, default.show_percentage, default.show_bubble_size,
            default.show_label_value_from_cell,
        ])

    @property
    def data_label_format(self) -> 'IDataLabelFormat':
        """Format of this specific label. Read-only."""
        from .DataLabelFormat import DataLabelFormat
        self._ensure_dlbl()
        fmt = DataLabelFormat()
        fmt._init_internal(self._elem, self._chart_part,
                           is_collection_default=False)
        return fmt

    @property
    def text_format(self) -> 'IChartTextFormat':
        """Chart text format. Read-only."""
        return self.data_label_format.text_format

    # ---- layout (x, y, width, height via c:layout/c:manualLayout) ----

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
        return self._read_c15_layout_val('w')

    @width.setter
    def width(self, value: float):
        self._write_c15_layout_val('w', value)

    @property
    def height(self) -> float:
        return self._read_c15_layout_val('h')

    @height.setter
    def height(self, value: float):
        self._write_c15_layout_val('h', value)

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def _manual_layout(self):
        """Return <c:manualLayout> or None."""
        layout = self._find('layout')
        if layout is None:
            return None
        return layout.find(self._c('manualLayout'))

    def _manual_layout_create(self):
        self._ensure_dlbl()
        layout = self._elem.find(self._c('layout'))
        if layout is None:
            layout = ET.Element(self._c('layout'))
            _insert_sorted(self._elem, layout, 'layout', _DLBL_ORDER)
        ml = layout.find(self._c('manualLayout'))
        if ml is None:
            ml = ET.SubElement(layout, self._c('manualLayout'))
        return ml

    def _read_layout_val(self, attr: str) -> float:
        ml = self._manual_layout()
        if ml is None:
            return 0.0
        elem = ml.find(self._c(attr))
        if elem is None:
            return 0.0
        try:
            return float(elem.get('val', '0'))
        except ValueError:
            return 0.0

    def _write_layout_val(self, attr: str, value: float):
        ml = self._manual_layout_create()
        elem = ml.find(self._c(attr))
        if elem is None:
            elem = ET.SubElement(ml, self._c(attr))
        elem.set('val', str(value))

    # Data label width/height live in a c15:layout extension, not in the base
    # <c:manualLayout>. Commercial Aspose uses this pattern and PowerPoint
    # expects w/h here for data-label sizing (as opposed to x/y positioning).

    def _read_c15_layout_val(self, attr: str) -> float:
        """Read w or h from the c15:layout extension."""
        if self._elem is None:
            return 0.0
        ml = self._c15_manual_layout()
        if ml is None:
            return 0.0
        elem = ml.find(self._c(attr))
        if elem is None:
            return 0.0
        try:
            return float(elem.get('val', '0'))
        except ValueError:
            return 0.0

    def _write_c15_layout_val(self, attr: str, value: float):
        """Write w or h to the c15:layout extension."""
        ml = self._c15_manual_layout_create()
        elem = ml.find(self._c(attr))
        if elem is None:
            elem = ET.SubElement(ml, self._c(attr))
        elem.set('val', str(value))

    def _c15_manual_layout(self):
        ext = self._find_c15_ext()
        if ext is None:
            return None
        c15_layout = ext.find(f'{{{C15_NS}}}layout')
        if c15_layout is None:
            return None
        return c15_layout.find(self._c('manualLayout'))

    def _c15_manual_layout_create(self):
        ext = self._find_or_create_c15_ext()
        c15_layout = ext.find(f'{{{C15_NS}}}layout')
        if c15_layout is None:
            c15_layout = ET.SubElement(ext, f'{{{C15_NS}}}layout')
        ml = c15_layout.find(self._c('manualLayout'))
        if ml is None:
            ml = ET.SubElement(c15_layout, self._c('manualLayout'))
        return ml

    def _find_c15_ext(self):
        if self._elem is None:
            return None
        ext_lst = self._elem.find(self._c('extLst'))
        if ext_lst is None:
            return None
        for ext in ext_lst.findall(self._c('ext')):
            if ext.get('uri') == C15_EXT_URI:
                return ext
        return None

    def _find_or_create_c15_ext(self):
        self._ensure_dlbl()
        ext_lst = self._elem.find(self._c('extLst'))
        if ext_lst is None:
            ext_lst = ET.Element(self._c('extLst'))
            _insert_sorted(self._elem, ext_lst, 'extLst', _DLBL_ORDER)
        ext = self._find_c15_ext()
        if ext is None:
            ext = ET.SubElement(
                ext_lst, self._c('ext'),
                attrib={'uri': C15_EXT_URI},
                nsmap={'c15': C15_NS},
            )
        return ext

    # ---- text_frame_for_overriding ----

    @property
    def text_frame_for_overriding(self) -> 'ITextFrame':
        """Overriding text frame for this label, or None."""
        if self._elem is None:
            return None
        tx = self._elem.find(self._c('tx'))
        if tx is None:
            return None
        rich = tx.find(self._c('rich'))
        if rich is None:
            return None
        from ..TextFrame import TextFrame
        tf = TextFrame()
        tf._init_internal(rich, self._chart_part, None)
        return tf

    def add_text_frame_for_overriding(self, text: str) -> 'ITextFrame':
        """Create or replace the overriding text frame with initial text."""
        self._ensure_dlbl()
        # Remove existing <c:tx>
        tx = self._elem.find(self._c('tx'))
        if tx is not None:
            self._elem.remove(tx)
        tx = ET.Element(self._c('tx'))
        _insert_sorted(self._elem, tx, 'tx', _DLBL_ORDER)
        rich = ET.SubElement(tx, self._c('rich'))
        ET.SubElement(rich, f'{self._ns_a}bodyPr')
        ET.SubElement(rich, f'{self._ns_a}lstStyle')
        p = ET.SubElement(rich, f'{self._ns_a}p')
        p_pr = ET.SubElement(p, f'{self._ns_a}pPr')
        ET.SubElement(p_pr, f'{self._ns_a}defRPr')
        if text:
            r = ET.SubElement(p, f'{self._ns_a}r')
            t = ET.SubElement(r, f'{self._ns_a}t')
            t.text = text
        else:
            ET.SubElement(p, f'{self._ns_a}endParaRPr',
                          attrib={'lang': 'en-US'})
        from ..TextFrame import TextFrame
        tf = TextFrame()
        tf._init_internal(rich, self._chart_part, None)
        return tf

    def get_actual_label_text(self) -> str:
        """Return the explicit override text when present, else empty string.

        Aspose computes auto-generated text from show_* flags at render time.
        FOSS does not render, so only the explicit override text is known.
        """
        tf = self.text_frame_for_overriding
        if tf is None:
            return ''
        try:
            return tf.text
        except Exception:
            return ''

    # ---- value_from_cell ----
    # Stored on the parent series, emitted at save time as a single series-level
    # c15:datalabelsRange extension (uri {02D57815-...}) — the form PowerPoint
    # expects.

    @property
    def value_from_cell(self) -> 'IChartDataCell':
        """Workbook cell whose value is used as label text. None when not set.

        Only meaningful while DataLabelFormat.show_label_value_from_cell is True.
        """
        series = self._parent_collection._parent_series
        cells = getattr(series, '_value_from_cell_cells', None)
        if not cells:
            return None
        return cells.get(self._index)

    @value_from_cell.setter
    def value_from_cell(self, value: 'ChartDataCell'):
        series = self._parent_collection._parent_series
        cells = getattr(series, '_value_from_cell_cells', None)
        if cells is None:
            cells = {}
            series._value_from_cell_cells = cells
        if value is None:
            cells.pop(self._index, None)
        else:
            cells[self._index] = value

    # ---- hide ----

    def hide(self) -> None:
        """Hide this label by setting <c:delete val='1'/>."""
        self._ensure_dlbl()
        # Clear all existing sub-elements except <c:idx>, add <c:delete>.
        for child in list(self._elem):
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local != 'idx':
                self._elem.remove(child)
        delete = ET.SubElement(self._elem, self._c('delete'))
        delete.set('val', '1')


# --- Module-level helpers ---

def _insert_sorted(parent, new_elem, local_name: str, order):
    """Insert new_elem under parent at its correct ordinal position."""
    try:
        target_idx = order.index(local_name)
    except ValueError:
        parent.append(new_elem)
        return
    parent_ns = '{' + parent.tag[1:parent.tag.find('}')] + '}' if '{' in parent.tag else ''
    later = {f'{parent_ns}{t}' for t in order[target_idx + 1:]}
    insert_before = None
    for child in parent:
        if child.tag in later:
            insert_before = child
            break
    if insert_before is not None:
        parent.insert(list(parent).index(insert_before), new_elem)
    else:
        parent.append(new_elem)


def _build_dlbl(index: int, ns_c: str):
    elem = ET.Element(f'{ns_c}dLbl')
    idx = ET.SubElement(elem, f'{ns_c}idx')
    idx.set('val', str(index))
    return elem


def _insert_dlbl_sorted(dlbls, new_dlbl, index: int, ns_c: str):
    """Insert a new <c:dLbl> at the right position (<c:dLbl> elements first, ordered by idx)."""
    # Find the first non-dLbl child to insert before.
    first_non_dlbl = None
    insert_after = None
    for child in dlbls:
        if child.tag == f'{ns_c}dLbl':
            idx_elem = child.find(f'{ns_c}idx')
            if idx_elem is not None:
                try:
                    child_idx = int(idx_elem.get('val', '0'))
                    if child_idx < index:
                        insert_after = child
                    else:
                        first_non_dlbl = child
                        break
                except ValueError:
                    pass
        else:
            first_non_dlbl = child
            break
    if insert_after is not None:
        pos = list(dlbls).index(insert_after) + 1
        dlbls.insert(pos, new_dlbl)
    elif first_non_dlbl is not None:
        dlbls.insert(list(dlbls).index(first_non_dlbl), new_dlbl)
    else:
        dlbls.append(new_dlbl)


def _seed_show_flags_from_defaults(dlbl, dlbls, ns_c: str) -> None:
    """Copy the 6 show_* flag values from the series-level dLbls into a new dLbl.

    Skips showLeaderLines — that one is only meaningful at the series level.
    If the series dLbls has no flag of a given name, seed with val='0'.
    """
    for tag in ('showLegendKey', 'showVal', 'showCatName',
                'showSerName', 'showPercent', 'showBubbleSize'):
        src = dlbls.find(f'{ns_c}{tag}')
        val = src.get('val', '0') if src is not None else '0'
        e = ET.SubElement(dlbl, f'{ns_c}{tag}')
        e.set('val', val)


def _col_index_to_letters(col_idx: int) -> str:
    """0-based column index to Excel letter (0=A)."""
    result = ''
    n = col_idx
    while True:
        n, rem = divmod(n, 26)
        result = chr(ord('A') + rem) + result
        if n == 0:
            break
        n -= 1
    return result
