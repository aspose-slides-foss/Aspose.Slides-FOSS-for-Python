from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ILineFormat import ILineFormat
from .ILineParamSource import ILineParamSource
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT

if TYPE_CHECKING:
    from .ILineFillFormat import ILineFillFormat
    from .ILineFormatEffectiveData import ILineFormatEffectiveData
    from .ISketchFormat import ISketchFormat
    from .LineAlignment import LineAlignment
    from .LineArrowheadLength import LineArrowheadLength
    from .LineArrowheadStyle import LineArrowheadStyle
    from .LineArrowheadWidth import LineArrowheadWidth
    from .LineCapStyle import LineCapStyle
    from .LineDashStyle import LineDashStyle
    from .LineJoinStyle import LineJoinStyle
    from .LineStyle import LineStyle
    from ._internal.pptx.slide_part import SlidePart

# OOXML dash preset -> LineDashStyle enum name
_DASH_MAP = {
    'solid': 'SOLID', 'dot': 'DOT', 'dash': 'DASH', 'lgDash': 'LARGE_DASH',
    'dashDot': 'DASH_DOT', 'lgDashDot': 'LARGE_DASH_DOT',
    'lgDashDotDot': 'LARGE_DASH_DOT_DOT', 'sysDash': 'SYSTEM_DASH',
    'sysDot': 'SYSTEM_DOT', 'sysDashDot': 'SYSTEM_DASH_DOT',
    'sysDashDotDot': 'SYSTEM_DASH_DOT_DOT',
}
_DASH_MAP_REV = {v: k for k, v in _DASH_MAP.items()}

# OOXML cap -> LineCapStyle enum name
_CAP_MAP = {'rnd': 'ROUND', 'sq': 'SQUARE', 'flat': 'FLAT'}
_CAP_MAP_REV = {v: k for k, v in _CAP_MAP.items()}

# OOXML cmpd -> LineStyle enum name
_CMPD_MAP = {
    'sng': 'SINGLE', 'dbl': 'THIN_THIN', 'thickThin': 'THICK_THIN',
    'thinThick': 'THIN_THICK', 'tri': 'THICK_BETWEEN_THIN',
}
_CMPD_MAP_REV = {v: k for k, v in _CMPD_MAP.items()}

# OOXML algn -> LineAlignment enum name
_ALGN_MAP = {'ctr': 'CENTER', 'in': 'INSET'}
_ALGN_MAP_REV = {v: k for k, v in _ALGN_MAP.items()}

# Arrowhead type -> LineArrowheadStyle enum name
_ARROW_TYPE_MAP = {
    'none': 'NONE', 'triangle': 'TRIANGLE', 'stealth': 'STEALTH',
    'diamond': 'DIAMOND', 'oval': 'OVAL', 'arrow': 'OPEN',
}
_ARROW_TYPE_MAP_REV = {v: k for k, v in _ARROW_TYPE_MAP.items()}

# Arrowhead width -> LineArrowheadWidth enum name
_ARROW_W_MAP = {'sm': 'NARROW', 'med': 'MEDIUM', 'lg': 'WIDE'}
_ARROW_W_MAP_REV = {v: k for k, v in _ARROW_W_MAP.items()}

# Arrowhead length -> LineArrowheadLength enum name
_ARROW_LEN_MAP = {'sm': 'SHORT', 'med': 'MEDIUM', 'lg': 'LONG'}
_ARROW_LEN_MAP_REV = {v: k for k, v in _ARROW_LEN_MAP.items()}


class LineFormat(PVIObject, ISlideComponent, IPresentationComponent, ILineFormat, ILineParamSource):
    """Represents format of a line."""

    def _init_internal(self, parent_element: ET._Element, slide_part: SlidePart, parent_slide, ln_tag: str | None = None) -> None:
        """
        Internal initialization.

        Args:
            parent_element: Any XML element that may contain <a:ln>
                (e.g., <p:spPr>, <a:rPr>).
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
            ln_tag: Optional custom tag to use instead of <a:ln> (e.g., <a:uLn> for underline).
        """
        self._parent_element = parent_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        if ln_tag is not None:
            self._ln_tag = ln_tag

    def _get_ln(self) -> ET._Element | None:
        """Get the <a:ln> element if it exists."""
        if not hasattr(self, '_parent_element'):
            return None
        tag = getattr(self, '_ln_tag', Elements.A_LN)
        return self._parent_element.find(tag)

    # OOXML CT_TableCellProperties child order for border lines within <a:tcPr>:
    # lnL → lnR → lnT → lnB → lnTlToBr → lnBlToTr → fill → cell3D → extLst
    _TC_PR_CHILD_ORDER = [
        Elements.A_LN_L, Elements.A_LN_R, Elements.A_LN_T, Elements.A_LN_B,
        Elements.A_LN_TL_TO_BR, Elements.A_LN_BL_TO_TR,
    ]

    def _ensure_ln(self) -> ET._Element:
        """Get or create the <a:ln> element at the correct position.

        OOXML requires spPr children in order: xfrm, geometry, fill, ln, effects.
        For tcPr children, border lines must be in order: lnL, lnR, lnT, lnB, lnTlToBr, lnBlToTr.
        """
        ln = self._get_ln()
        if ln is not None:
            return ln
        tag = getattr(self, '_ln_tag', Elements.A_LN)
        el = ET.Element(tag)
        # For table cell border elements, use the tcPr child ordering
        if tag in self._TC_PR_CHILD_ORDER:
            new_rank = self._TC_PR_CHILD_ORDER.index(tag)
            for i, child in enumerate(self._parent_element):
                try:
                    child_rank = self._TC_PR_CHILD_ORDER.index(child.tag)
                except ValueError:
                    # Non-border child (fill, cell3D, extLst) comes after all borders
                    self._parent_element.insert(i, el)
                    return el
                if child_rank > new_rank:
                    self._parent_element.insert(i, el)
                    return el
            self._parent_element.append(el)
            return el
        # Default: insert after fill elements, before effects
        insert_before = None
        for child in self._parent_element:
            if child.tag in (f"{NS.A}effectLst", f"{NS.A}effectDag",
                             f"{NS.A}scene3d", f"{NS.A}sp3d", f"{NS.A}extLst"):
                insert_before = child
                break
        if insert_before is not None:
            idx = list(self._parent_element).index(insert_before)
            self._parent_element.insert(idx, el)
        else:
            self._parent_element.append(el)
        return el

    # OOXML CT_LineProperties child order within <a:ln>:
    # fill → prstDash/custDash → round/bevel/miter → headEnd → tailEnd → extLst
    _LN_CHILD_ORDER = [
        Elements.A_NO_FILL, Elements.A_SOLID_FILL, Elements.A_GRAD_FILL, Elements.A_PATT_FILL,
        Elements.A_PRST_DASH, Elements.A_CUST_DASH,
        Elements.A_ROUND, Elements.A_BEVEL, Elements.A_MITER,
        Elements.A_HEAD_END, Elements.A_TAIL_END,
        f"{NS.A}extLst",
    ]

    def _insert_ln_child(self, ln: ET._Element, tag: str, **attribs) -> ET._Element:
        """Insert a child element into <a:ln> at the correct OOXML position."""
        new_el = ET.Element(tag, **attribs)
        try:
            new_rank = self._LN_CHILD_ORDER.index(tag)
        except ValueError:
            ln.append(new_el)
            return new_el
        for i, child in enumerate(ln):
            try:
                child_rank = self._LN_CHILD_ORDER.index(child.tag)
            except ValueError:
                continue
            if child_rank > new_rank:
                ln.insert(i, new_el)
                return new_el
        ln.append(new_el)
        return new_el

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def is_format_not_defined(self) -> bool:
        """Returns true if line format is not defined (as just created, default). Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._get_ln()
        if ln is None:
            return True
        # Also check if ln has no attributes and no children
        return len(ln.attrib) == 0 and len(ln) == 0

    @property
    def fill_format(self) -> ILineFillFormat:
        """Returns the fill format of a line. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineFillFormat import LineFillFormat
        ln = self._ensure_ln()
        lff = LineFillFormat()
        lff._init_internal(ln, self._slide_part, self._parent_slide)
        return lff


    @property
    def width(self) -> float:
        """Returns or sets the width of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._get_ln()
        if ln is None:
            return 0.75  # Default line width in points
        w = ln.get('w')
        if w is None:
            return 0.75
        return int(w) / EMU_PER_POINT

    @width.setter
    def width(self, value: float):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._ensure_ln()
        ln.set('w', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def dash_style(self) -> LineDashStyle:
        """Returns or sets the line dash style. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineDashStyle import LineDashStyle
        ln = self._get_ln()
        if ln is None:
            return LineDashStyle.NOT_DEFINED
        # Check for custom dash first
        cust_dash = ln.find(Elements.A_CUST_DASH)
        if cust_dash is not None:
            return LineDashStyle.CUSTOM
        prst_dash = ln.find(Elements.A_PRST_DASH)
        if prst_dash is None:
            return LineDashStyle.NOT_DEFINED
        val = prst_dash.get('val', '')
        name = _DASH_MAP.get(val)
        return LineDashStyle[name] if name else LineDashStyle.NOT_DEFINED

    @dash_style.setter
    def dash_style(self, value: LineDashStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineDashStyle import LineDashStyle
        ln = self._ensure_ln()
        # Remove existing dash elements
        for tag in [Elements.A_PRST_DASH, Elements.A_CUST_DASH]:
            el = ln.find(tag)
            if el is not None:
                ln.remove(el)
        if value == LineDashStyle.NOT_DEFINED:
            pass  # No dash element needed
        elif value == LineDashStyle.CUSTOM:
            self._insert_ln_child(ln, Elements.A_CUST_DASH)
        else:
            ooxml_val = _DASH_MAP_REV.get(value.name)
            if ooxml_val:
                self._insert_ln_child(ln, Elements.A_PRST_DASH, val=ooxml_val)
        self._save()

    @property
    def custom_dash_pattern(self) -> list[float]:
        """Returns or sets the custom dash pattern. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._get_ln()
        if ln is None:
            return []
        cust_dash = ln.find(Elements.A_CUST_DASH)
        if cust_dash is None:
            return []
        result = []
        for ds in cust_dash:
            d = ds.get('d', '0')
            sp = ds.get('sp', '0')
            result.append(int(d) / 100000.0)
            result.append(int(sp) / 100000.0)
        return result

    @custom_dash_pattern.setter
    def custom_dash_pattern(self, value: list[float]):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._ensure_ln()
        cust_dash = ln.find(Elements.A_CUST_DASH)
        if cust_dash is None:
            # Remove preset dash
            prst_dash = ln.find(Elements.A_PRST_DASH)
            if prst_dash is not None:
                ln.remove(prst_dash)
            cust_dash = self._insert_ln_child(ln, Elements.A_CUST_DASH)
        else:
            cust_dash.clear()
        # Value is pairs of [dash, space, dash, space, ...]
        for i in range(0, len(value) - 1, 2):
            ET.SubElement(cust_dash, f"{NS.A}ds",
                          d=str(int(round(value[i] * 100000))),
                          sp=str(int(round(value[i + 1] * 100000))))
        self._save()

    @property
    def cap_style(self) -> LineCapStyle:
        """Returns or sets the line cap style. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineCapStyle import LineCapStyle
        ln = self._get_ln()
        if ln is None:
            return LineCapStyle.NOT_DEFINED
        val = ln.get('cap')
        if val is None:
            return LineCapStyle.NOT_DEFINED
        name = _CAP_MAP.get(val)
        return LineCapStyle[name] if name else LineCapStyle.NOT_DEFINED

    @cap_style.setter
    def cap_style(self, value: LineCapStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineCapStyle import LineCapStyle
        ln = self._ensure_ln()
        if value == LineCapStyle.NOT_DEFINED:
            if 'cap' in ln.attrib:
                del ln.attrib['cap']
        else:
            ooxml_val = _CAP_MAP_REV.get(value.name)
            if ooxml_val:
                ln.set('cap', ooxml_val)
        self._save()

    @property
    def style(self) -> LineStyle:
        """Returns or sets the line style. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineStyle import LineStyle
        ln = self._get_ln()
        if ln is None:
            return LineStyle.NOT_DEFINED
        val = ln.get('cmpd')
        if val is None:
            return LineStyle.NOT_DEFINED
        name = _CMPD_MAP.get(val)
        return LineStyle[name] if name else LineStyle.NOT_DEFINED

    @style.setter
    def style(self, value: LineStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineStyle import LineStyle
        ln = self._ensure_ln()
        if value == LineStyle.NOT_DEFINED:
            if 'cmpd' in ln.attrib:
                del ln.attrib['cmpd']
        else:
            ooxml_val = _CMPD_MAP_REV.get(value.name)
            if ooxml_val:
                ln.set('cmpd', ooxml_val)
        self._save()

    @property
    def alignment(self) -> LineAlignment:
        """Returns or sets the line alignment. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineAlignment import LineAlignment
        ln = self._get_ln()
        if ln is None:
            return LineAlignment.NOT_DEFINED
        val = ln.get('algn')
        if val is None:
            return LineAlignment.NOT_DEFINED
        name = _ALGN_MAP.get(val)
        return LineAlignment[name] if name else LineAlignment.NOT_DEFINED

    @alignment.setter
    def alignment(self, value: LineAlignment):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineAlignment import LineAlignment
        ln = self._ensure_ln()
        if value == LineAlignment.NOT_DEFINED:
            if 'algn' in ln.attrib:
                del ln.attrib['algn']
        else:
            ooxml_val = _ALGN_MAP_REV.get(value.name)
            if ooxml_val:
                ln.set('algn', ooxml_val)
        self._save()

    @property
    def join_style(self) -> LineJoinStyle:
        """Returns or sets the lines join style. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineJoinStyle import LineJoinStyle
        ln = self._get_ln()
        if ln is None:
            return LineJoinStyle.NOT_DEFINED
        if ln.find(Elements.A_ROUND) is not None:
            return LineJoinStyle.ROUND
        if ln.find(Elements.A_BEVEL) is not None:
            return LineJoinStyle.BEVEL
        if ln.find(Elements.A_MITER) is not None:
            return LineJoinStyle.MITER
        return LineJoinStyle.NOT_DEFINED

    @join_style.setter
    def join_style(self, value: LineJoinStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineJoinStyle import LineJoinStyle
        ln = self._ensure_ln()
        # Remove existing join elements
        for tag in [Elements.A_ROUND, Elements.A_BEVEL, Elements.A_MITER]:
            el = ln.find(tag)
            if el is not None:
                ln.remove(el)
        if value == LineJoinStyle.ROUND:
            self._insert_ln_child(ln, Elements.A_ROUND)
        elif value == LineJoinStyle.BEVEL:
            self._insert_ln_child(ln, Elements.A_BEVEL)
        elif value == LineJoinStyle.MITER:
            self._insert_ln_child(ln, Elements.A_MITER)
        self._save()

    @property
    def miter_limit(self) -> float:
        """Returns or sets the miter limit of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._get_ln()
        if ln is None:
            return 0.0
        miter = ln.find(Elements.A_MITER)
        if miter is None:
            return 0.0
        lim = miter.get('lim')
        if lim is None:
            return 0.0
        return int(lim) / 100000.0

    @miter_limit.setter
    def miter_limit(self, value: float):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ln = self._ensure_ln()
        miter = ln.find(Elements.A_MITER)
        if miter is None:
            # Remove other join styles and add miter
            for tag in [Elements.A_ROUND, Elements.A_BEVEL]:
                el = ln.find(tag)
                if el is not None:
                    ln.remove(el)
            miter = self._insert_ln_child(ln, Elements.A_MITER)
        miter.set('lim', str(int(round(value * 100000))))
        self._save()

    def _get_arrow_attr(self, end_tag: str, attr: str) -> str | None:
        """Get an arrowhead attribute value."""
        ln = self._get_ln()
        if ln is None:
            return None
        end_elem = ln.find(end_tag)
        if end_elem is None:
            return None
        return end_elem.get(attr)

    def _set_arrow_attr(self, end_tag: str, attr: str, value: str | None) -> None:
        """Set an arrowhead attribute value."""
        ln = self._ensure_ln()
        end_elem = ln.find(end_tag)
        if end_elem is None:
            end_elem = self._insert_ln_child(ln, end_tag)
        if value is None:
            if attr in end_elem.attrib:
                del end_elem.attrib[attr]
        else:
            end_elem.set(attr, value)
        self._save()

    @property
    def begin_arrowhead_style(self) -> LineArrowheadStyle:
        """Returns or sets the arrowhead style at the beginning of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadStyle import LineArrowheadStyle
        val = self._get_arrow_attr(Elements.A_HEAD_END, 'type')
        if val is None:
            return LineArrowheadStyle.NOT_DEFINED
        name = _ARROW_TYPE_MAP.get(val)
        return LineArrowheadStyle[name] if name else LineArrowheadStyle.NOT_DEFINED

    @begin_arrowhead_style.setter
    def begin_arrowhead_style(self, value: LineArrowheadStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadStyle import LineArrowheadStyle
        if value == LineArrowheadStyle.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_HEAD_END, 'type', None)
        else:
            ooxml_val = _ARROW_TYPE_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_HEAD_END, 'type', ooxml_val)

    @property
    def end_arrowhead_style(self) -> LineArrowheadStyle:
        """Returns or sets the arrowhead style at the end of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadStyle import LineArrowheadStyle
        val = self._get_arrow_attr(Elements.A_TAIL_END, 'type')
        if val is None:
            return LineArrowheadStyle.NOT_DEFINED
        name = _ARROW_TYPE_MAP.get(val)
        return LineArrowheadStyle[name] if name else LineArrowheadStyle.NOT_DEFINED

    @end_arrowhead_style.setter
    def end_arrowhead_style(self, value: LineArrowheadStyle):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadStyle import LineArrowheadStyle
        if value == LineArrowheadStyle.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_TAIL_END, 'type', None)
        else:
            ooxml_val = _ARROW_TYPE_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_TAIL_END, 'type', ooxml_val)

    @property
    def begin_arrowhead_width(self) -> LineArrowheadWidth:
        """Returns or sets the arrowhead width at the beginning of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadWidth import LineArrowheadWidth
        val = self._get_arrow_attr(Elements.A_HEAD_END, 'w')
        if val is None:
            return LineArrowheadWidth.NOT_DEFINED
        name = _ARROW_W_MAP.get(val)
        return LineArrowheadWidth[name] if name else LineArrowheadWidth.NOT_DEFINED

    @begin_arrowhead_width.setter
    def begin_arrowhead_width(self, value: LineArrowheadWidth):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadWidth import LineArrowheadWidth
        if value == LineArrowheadWidth.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_HEAD_END, 'w', None)
        else:
            ooxml_val = _ARROW_W_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_HEAD_END, 'w', ooxml_val)

    @property
    def end_arrowhead_width(self) -> LineArrowheadWidth:
        """Returns or sets the arrowhead width at the end of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadWidth import LineArrowheadWidth
        val = self._get_arrow_attr(Elements.A_TAIL_END, 'w')
        if val is None:
            return LineArrowheadWidth.NOT_DEFINED
        name = _ARROW_W_MAP.get(val)
        return LineArrowheadWidth[name] if name else LineArrowheadWidth.NOT_DEFINED

    @end_arrowhead_width.setter
    def end_arrowhead_width(self, value: LineArrowheadWidth):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadWidth import LineArrowheadWidth
        if value == LineArrowheadWidth.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_TAIL_END, 'w', None)
        else:
            ooxml_val = _ARROW_W_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_TAIL_END, 'w', ooxml_val)

    @property
    def begin_arrowhead_length(self) -> LineArrowheadLength:
        """Returns or sets the arrowhead length at the beginning of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadLength import LineArrowheadLength
        val = self._get_arrow_attr(Elements.A_HEAD_END, 'len')
        if val is None:
            return LineArrowheadLength.NOT_DEFINED
        name = _ARROW_LEN_MAP.get(val)
        return LineArrowheadLength[name] if name else LineArrowheadLength.NOT_DEFINED

    @begin_arrowhead_length.setter
    def begin_arrowhead_length(self, value: LineArrowheadLength):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadLength import LineArrowheadLength
        if value == LineArrowheadLength.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_HEAD_END, 'len', None)
        else:
            ooxml_val = _ARROW_LEN_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_HEAD_END, 'len', ooxml_val)

    @property
    def end_arrowhead_length(self) -> LineArrowheadLength:
        """Returns or sets the arrowhead length at the end of a line. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadLength import LineArrowheadLength
        val = self._get_arrow_attr(Elements.A_TAIL_END, 'len')
        if val is None:
            return LineArrowheadLength.NOT_DEFINED
        name = _ARROW_LEN_MAP.get(val)
        return LineArrowheadLength[name] if name else LineArrowheadLength.NOT_DEFINED

    @end_arrowhead_length.setter
    def end_arrowhead_length(self, value: LineArrowheadLength):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LineArrowheadLength import LineArrowheadLength
        if value == LineArrowheadLength.NOT_DEFINED:
            self._set_arrow_attr(Elements.A_TAIL_END, 'len', None)
        else:
            ooxml_val = _ARROW_LEN_MAP_REV.get(value.name)
            self._set_arrow_attr(Elements.A_TAIL_END, 'len', ooxml_val)



