from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from .LegendDataLabelPosition import LegendDataLabelPosition
from .IDataLabelFormat import IDataLabelFormat

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .ChartTextFormat import ChartTextFormat
    from .Format import Format
    from .IChartTextFormat import IChartTextFormat
    from .IFormat import IFormat


# XML val <-> enum mapping for <c:dLblPos>
_POS_ENUM_TO_XML = {
    LegendDataLabelPosition.BOTTOM: 'b',
    LegendDataLabelPosition.BEST_FIT: 'bestFit',
    LegendDataLabelPosition.CENTER: 'ctr',
    LegendDataLabelPosition.INSIDE_BASE: 'inBase',
    LegendDataLabelPosition.INSIDE_END: 'inEnd',
    LegendDataLabelPosition.LEFT: 'l',
    LegendDataLabelPosition.OUTSIDE_END: 'outEnd',
    LegendDataLabelPosition.RIGHT: 'r',
    LegendDataLabelPosition.TOP: 't',
}
_POS_XML_TO_ENUM = {v: k for k, v in _POS_ENUM_TO_XML.items()}

# Bool property tag -> default when element absent.
_SHOW_FLAG_DEFAULTS = {
    'showLegendKey': False,
    'showVal': False,
    'showCatName': False,
    'showSerName': False,
    'showPercent': False,
    'showBubbleSize': False,
    'showLeaderLines': False,
}

# OOXML ordering of <c:dLbls>/<c:dLbl> child elements, after any <c:dLbl>,
# <c:idx>, <c:layout>, <c:tx>. Used to place new children in a valid spot.
_ORDER_AFTER_TX = (
    'numFmt', 'spPr', 'txPr', 'dLblPos',
    'showLegendKey', 'showVal', 'showCatName', 'showSerName',
    'showPercent', 'showBubbleSize', 'separator',
    'showLeaderLines', 'leaderLines', 'extLst',
)

C15_NS = 'http://schemas.microsoft.com/office/drawing/2012/chart'
C15_EXT_URI = '{CE6537A1-D6FC-4f65-9D91-7224C49458BB}'


class DataLabelFormat(IDataLabelFormat):
    """Represents formatting options for DataLabel.

    Wraps either a <c:dLbls> (default/collection-level format) or
    <c:dLbl> (per-data-point override) element.
    """

    def _init_internal(self, parent_element, chart_part: 'ChartPart',
                       is_collection_default: bool):
        """
        Args:
            parent_element: <c:dLbls> or <c:dLbl>.
            chart_part: owning chart part.
            is_collection_default: True when parent is <c:dLbls>; False for <c:dLbl>.
        """
        from .._internal.pptx.constants import NS
        self._elem = parent_element
        self._chart_part = chart_part
        self._is_collection_default = is_collection_default
        self._ns_c = NS.C
        self._ns_a = NS.A

    # ---- internal element helpers ----

    def _c(self, local: str) -> str:
        return f'{self._ns_c}{local}'

    def _find(self, local: str):
        return self._elem.find(self._c(local))

    def _find_or_create(self, local: str):
        child = self._find(local)
        if child is None:
            child = ET.Element(self._c(local))
            self._insert_ordered(child, local)
        return child

    def _insert_ordered(self, new_elem, local: str) -> None:
        """Insert a child element in OOXML-required order."""
        try:
            target_idx = _ORDER_AFTER_TX.index(local)
        except ValueError:
            self._elem.append(new_elem)
            return
        # Collect children that should come AFTER new_elem, find first.
        later_tags = {self._c(t) for t in _ORDER_AFTER_TX[target_idx + 1:]}
        # Also: all children that come BEFORE in the schema must be preserved.
        # We find the first existing child whose local name is in later_tags.
        insert_before = None
        for child in self._elem:
            if child.tag in later_tags:
                insert_before = child
                break
        if insert_before is not None:
            self._elem.insert(list(self._elem).index(insert_before), new_elem)
        else:
            self._elem.append(new_elem)

    def _get_bool(self, local: str, default: bool) -> bool:
        e = self._find(local)
        if e is None:
            return default
        return e.get('val', '1') in ('1', 'true')

    def _set_bool(self, local: str, value: bool) -> None:
        self._materialize_show_defaults()
        e = self._find_or_create(local)
        e.set('val', '1' if value else '0')

    # The 7 visibility flags a <c:dLbls> may carry. Order matters (OOXML schema
    # requires this relative order before <c:separator>/<c:leaderLines>).
    _SHOW_FLAGS = (
        'showLegendKey', 'showVal', 'showCatName', 'showSerName',
        'showPercent', 'showBubbleSize', 'showLeaderLines',
    )

    def _materialize_show_defaults(self) -> None:
        """Write explicit val='0' for every show_* flag missing from the element.

        Only applied on collection-level <c:dLbls>, not per-point <c:dLbl>.
        Absent show_* elements can inherit chart-type-level defaults in
        PowerPoint, so we pin them to FALSE when the user touches the format.
        """
        if not self._is_collection_default:
            return
        for tag in self._SHOW_FLAGS:
            if self._find(tag) is None:
                e = ET.Element(self._c(tag))
                e.set('val', '0')
                self._insert_ordered(e, tag)

    # ---- show_* flags ----

    @property
    def show_legend_key(self) -> bool:
        """True if the data label legend key is visible. Read/write."""
        return self._get_bool('showLegendKey', _SHOW_FLAG_DEFAULTS['showLegendKey'])

    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        self._set_bool('showLegendKey', value)

    @property
    def show_value(self) -> bool:
        """True displays the value. Read/write."""
        return self._get_bool('showVal', _SHOW_FLAG_DEFAULTS['showVal'])

    @show_value.setter
    def show_value(self, value: bool):
        self._set_bool('showVal', value)

    @property
    def show_category_name(self) -> bool:
        """True displays the category name. Read/write."""
        return self._get_bool('showCatName', _SHOW_FLAG_DEFAULTS['showCatName'])

    @show_category_name.setter
    def show_category_name(self, value: bool):
        self._set_bool('showCatName', value)

    @property
    def show_series_name(self) -> bool:
        """True displays the series name. Read/write."""
        return self._get_bool('showSerName', _SHOW_FLAG_DEFAULTS['showSerName'])

    @show_series_name.setter
    def show_series_name(self, value: bool):
        self._set_bool('showSerName', value)

    @property
    def show_percentage(self) -> bool:
        """True displays the percentage value. Read/write."""
        return self._get_bool('showPercent', _SHOW_FLAG_DEFAULTS['showPercent'])

    @show_percentage.setter
    def show_percentage(self, value: bool):
        self._set_bool('showPercent', value)

    @property
    def show_bubble_size(self) -> bool:
        """True displays the bubble size. Read/write."""
        return self._get_bool('showBubbleSize', _SHOW_FLAG_DEFAULTS['showBubbleSize'])

    @show_bubble_size.setter
    def show_bubble_size(self, value: bool):
        self._set_bool('showBubbleSize', value)

    @property
    def show_leader_lines(self) -> bool:
        """True displays leader lines. Read/write."""
        return self._get_bool('showLeaderLines', _SHOW_FLAG_DEFAULTS['showLeaderLines'])

    @show_leader_lines.setter
    def show_leader_lines(self, value: bool):
        self._set_bool('showLeaderLines', value)

    # ---- position (c:dLblPos) ----

    @property
    def position(self) -> LegendDataLabelPosition:
        """Position of the data label. Read/write."""
        e = self._find('dLblPos')
        if e is None:
            return LegendDataLabelPosition.NOT_DEFINED
        val = e.get('val')
        return _POS_XML_TO_ENUM.get(val, LegendDataLabelPosition.NOT_DEFINED)

    @position.setter
    def position(self, value: LegendDataLabelPosition):
        if value == LegendDataLabelPosition.NOT_DEFINED:
            e = self._find('dLblPos')
            if e is not None:
                self._elem.remove(e)
            return
        xml_val = _POS_ENUM_TO_XML.get(value)
        if xml_val is None:
            return
        self._materialize_show_defaults()
        e = self._find_or_create('dLblPos')
        e.set('val', xml_val)

    # ---- number format ----

    @property
    def number_format(self) -> str:
        """Format string for DataLabels. Read/write."""
        e = self._find('numFmt')
        if e is None:
            return 'General'
        return e.get('formatCode', 'General')

    @number_format.setter
    def number_format(self, value: str):
        self._materialize_show_defaults()
        e = self._find_or_create('numFmt')
        e.set('formatCode', value if value is not None else 'General')
        if 'sourceLinked' not in e.attrib:
            e.set('sourceLinked', '0')

    @property
    def is_number_format_linked_to_source(self) -> bool:
        """Whether number format is linked to the data source. Read/write."""
        e = self._find('numFmt')
        if e is None:
            return True
        return e.get('sourceLinked', '0') in ('1', 'true')

    @is_number_format_linked_to_source.setter
    def is_number_format_linked_to_source(self, value: bool):
        self._materialize_show_defaults()
        e = self._find_or_create('numFmt')
        e.set('sourceLinked', '1' if value else '0')
        if 'formatCode' not in e.attrib:
            e.set('formatCode', 'General')

    # ---- separator ----

    @property
    def separator(self) -> str:
        """Separator used between label fields. Read/write."""
        e = self._find('separator')
        if e is None:
            return ''
        return e.text or ''

    @separator.setter
    def separator(self, value: str):
        if value is None or value == '':
            e = self._find('separator')
            if e is not None:
                self._elem.remove(e)
            return
        self._materialize_show_defaults()
        e = self._find_or_create('separator')
        e.text = value

    # ---- format (fill / line / effect via <c:spPr>) ----

    @property
    def format(self) -> 'IFormat':
        """Fill, line, and effect formatting of the label area. Read-only."""
        from .Format import Format
        self._materialize_show_defaults()
        f = Format()
        f._init_internal(self._shape_host(), self._chart_part)
        return f

    def _shape_host(self):
        """Parent element for <c:spPr>. Kept inside dLbls/dLbl directly."""
        return self._elem

    # ---- text_format (via <c:txPr>) ----

    @property
    def text_format(self) -> 'IChartTextFormat':
        """Chart text format. Read-only."""
        from .ChartTextFormat import ChartTextFormat
        self._materialize_show_defaults()
        ctf = ChartTextFormat()
        ctf._init_internal(self._elem, self._chart_part)
        return ctf

    # ---- show_label_value_from_cell (c15 extension) ----

    @property
    def show_label_value_from_cell(self) -> bool:
        """True displays label text sourced from workbook cell(s)."""
        ext = self._find_c15_ext()
        if ext is None:
            return False
        sdr = ext.find(f'{{{C15_NS}}}showDataLabelsRange')
        if sdr is None:
            return False
        return sdr.get('val', '1') in ('1', 'true')

    @show_label_value_from_cell.setter
    def show_label_value_from_cell(self, value: bool):
        if value:
            self._materialize_show_defaults()
            ext = self._find_or_create_c15_ext()
            sdr = ext.find(f'{{{C15_NS}}}showDataLabelsRange')
            if sdr is None:
                sdr = ET.SubElement(ext, f'{{{C15_NS}}}showDataLabelsRange')
            sdr.set('val', '1')
        else:
            ext = self._find_c15_ext()
            if ext is not None:
                sdr = ext.find(f'{{{C15_NS}}}showDataLabelsRange')
                if sdr is not None:
                    ext.remove(sdr)
                self._cleanup_empty_ext()

    # ---- extLst helpers ----

    def _find_c15_ext(self):
        ext_lst = self._find('extLst')
        if ext_lst is None:
            return None
        for ext in ext_lst.findall(self._c('ext')):
            if ext.get('uri') == C15_EXT_URI:
                return ext
        return None

    def _find_or_create_c15_ext(self):
        ext_lst = self._find('extLst')
        if ext_lst is None:
            ext_lst = ET.Element(self._c('extLst'))
            self._insert_ordered(ext_lst, 'extLst')
        ext = self._find_c15_ext()
        if ext is None:
            ext = ET.SubElement(
                ext_lst, self._c('ext'),
                attrib={'uri': C15_EXT_URI},
                nsmap={'c15': C15_NS},
            )
        return ext

    def _cleanup_empty_ext(self):
        ext_lst = self._find('extLst')
        if ext_lst is None:
            return
        to_remove = [e for e in ext_lst.findall(self._c('ext')) if len(e) == 0]
        for e in to_remove:
            ext_lst.remove(e)
        if len(ext_lst) == 0:
            self._elem.remove(ext_lst)
