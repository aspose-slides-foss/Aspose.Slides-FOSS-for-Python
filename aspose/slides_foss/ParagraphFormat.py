from __future__ import annotations
import math
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IParagraphFormat import IParagraphFormat
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT

if TYPE_CHECKING:
    from .FontAlignment import FontAlignment
    from .IBulletFormat import IBulletFormat
    from .IParagraphFormatEffectiveData import IParagraphFormatEffectiveData
    from .IPortionFormat import IPortionFormat
    from .ITabCollection import ITabCollection
    from .NullableBool import NullableBool
    from .TextAlignment import TextAlignment

# OOXML alignment attribute values -> TextAlignment enum names
_ALIGNMENT_MAP = {
    'l': 'LEFT', 'ctr': 'CENTER', 'r': 'RIGHT',
    'just': 'JUSTIFY', 'justLow': 'JUSTIFY_LOW', 'dist': 'DISTRIBUTED',
}
_ALIGNMENT_MAP_REV = {v: k for k, v in _ALIGNMENT_MAP.items()}

# OOXML fontAlign attribute values -> FontAlignment enum names
_FONT_ALIGN_MAP = {
    'auto': 'AUTOMATIC', 't': 'TOP', 'ctr': 'CENTER',
    'b': 'BOTTOM', 'base': 'BASELINE',
}
_FONT_ALIGN_MAP_REV = {v: k for k, v in _FONT_ALIGN_MAP.items()}

# OOXML schema order for <a:pPr> child elements (CT_TextParagraphProperties).
# Each entry is a set of mutually-exclusive tags that occupy that position.
_PPR_CHILD_ORDER = [
    {Elements.A_LN_SPC},                                                      # 0: lnSpc
    {Elements.A_SPC_BEF},                                                     # 1: spcBef
    {Elements.A_SPC_AFT},                                                     # 2: spcAft
    {Elements.A_BU_CLR_TX, Elements.A_BU_CLR},                                # 3: buClrTx / buClr
    {Elements.A_BU_SZ_TX, Elements.A_BU_SZ_PCT, Elements.A_BU_SZ_PTS},       # 4: buSzTx / buSzPct / buSzPts
    {Elements.A_BU_FONT_TX, Elements.A_BU_FONT},                              # 5: buFontTx / buFont
    {Elements.A_BU_NONE, Elements.A_BU_AUTO_NUM, Elements.A_BU_CHAR, Elements.A_BU_BLIP},  # 6: bullet type
    {Elements.A_TAB_LST},                                                     # 7: tabLst
    {Elements.A_DEF_R_PR},                                                    # 8: defRPr
    {Elements.A_EXT_LST},                                                     # 9: extLst
]

# Build a tag -> position index for fast lookup
_PPR_TAG_INDEX = {}
for _i, _tags in enumerate(_PPR_CHILD_ORDER):
    for _tag in _tags:
        _PPR_TAG_INDEX[_tag] = _i


def _ppr_insert_child(ppr: ET._Element, tag: str, attrib: dict = None) -> ET._Element:
    """Create and insert a child element into <a:pPr> at the correct schema position."""
    target_pos = _PPR_TAG_INDEX.get(tag, 999)
    insert_before = None
    for child in ppr:
        child_pos = _PPR_TAG_INDEX.get(child.tag, 999)
        if child_pos > target_pos:
            insert_before = child
            break
    el = ET.Element(tag, attrib=attrib or {})
    if insert_before is not None:
        insert_before.addprevious(el)
    else:
        ppr.append(el)
    return el


class ParagraphFormat(PVIObject, ISlideComponent, IPresentationComponent, IParagraphFormat):
    """This class contains the paragraph formatting properties. Unlike , all properties of this class are writeable."""
    def __init__(self):
        # Create a detached <a:pPr> so the object works standalone.
        self._ppr_element = ET.Element(Elements.A_P_PR)
        self._slide_part = None
        self._parent_slide = None

    def _init_internal(self, ppr_element, slide_part, parent_slide):
        self._ppr_element = ppr_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    def _save(self):
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    # --- Helper for NullableBool attributes ---

    def _get_nullable_bool_attr(self, attr):
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return NullableBool.NOT_DEFINED
        val = self._ppr_element.get(attr)
        if val is None:
            return NullableBool.NOT_DEFINED
        return NullableBool.TRUE if val == '1' else NullableBool.FALSE

    def _set_nullable_bool_attr(self, attr, value):
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == NullableBool.NOT_DEFINED:
            if attr in self._ppr_element.attrib:
                del self._ppr_element.attrib[attr]
        else:
            self._ppr_element.set(attr, '1' if value == NullableBool.TRUE else '0')
        self._save()

    # --- Spacing helpers ---

    def _get_spacing(self, tag):
        """Read spacing from a child element (lnSpc, spcBef, spcAft).
        Positive return = percentage, negative = points."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return float('nan')
        el = self._ppr_element.find(tag)
        if el is None:
            return float('nan')
        pct = el.find(Elements.A_SPC_PCT)
        if pct is not None:
            val = pct.get('val')
            if val is not None:
                return int(val) / 1000.0
        pts = el.find(Elements.A_SPC_PTS)
        if pts is not None:
            val = pts.get('val')
            if val is not None:
                return -(int(val) / 100.0)
        return float('nan')

    def _set_spacing(self, tag, value):
        """Write spacing to a child element.
        Positive value = percentage (spcPct), negative = points (spcPts)."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        el = self._ppr_element.find(tag)
        if math.isnan(value):
            if el is not None:
                self._ppr_element.remove(el)
        else:
            if el is None:
                el = _ppr_insert_child(self._ppr_element, tag)
            # Remove existing children
            for child in list(el):
                el.remove(child)
            if value >= 0:
                ET.SubElement(el, Elements.A_SPC_PCT, attrib={'val': str(int(round(value * 1000)))})
            else:
                ET.SubElement(el, Elements.A_SPC_PTS, attrib={'val': str(int(round(-value * 100)))})
        self._save()

    # --- Alignment ---

    @property
    def alignment(self) -> TextAlignment:
        """Returns or sets the text alignment in a paragraph with no inheritance. Read/write ."""
        from .TextAlignment import TextAlignment
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return TextAlignment.NOT_DEFINED
        val = self._ppr_element.get('algn')
        if val is None:
            return TextAlignment.NOT_DEFINED
        name = _ALIGNMENT_MAP.get(val)
        return TextAlignment[name] if name else TextAlignment.NOT_DEFINED

    @alignment.setter
    def alignment(self, value: TextAlignment):
        from .TextAlignment import TextAlignment
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == TextAlignment.NOT_DEFINED:
            if 'algn' in self._ppr_element.attrib:
                del self._ppr_element.attrib['algn']
        else:
            ooxml_val = _ALIGNMENT_MAP_REV.get(value.name)
            if ooxml_val:
                self._ppr_element.set('algn', ooxml_val)
        self._save()

    # --- Spacing properties ---

    @property
    def space_within(self) -> float:
        """Returns or sets the amount of space between base lines in a paragraph. Positive value means percentage, negative - size in points. No inheritance applied. Read/write ."""
        return self._get_spacing(Elements.A_LN_SPC)

    @space_within.setter
    def space_within(self, value: float):
        self._set_spacing(Elements.A_LN_SPC, value)

    @property
    def space_before(self) -> float:
        """Returns or sets the amount of space before the first line in a paragraph with no inheritance. A positive value specifies the percentage of the font size that the white space should be. A negative value specifies the size of the white space in point size. Read/write ."""
        return self._get_spacing(Elements.A_SPC_BEF)

    @space_before.setter
    def space_before(self, value: float):
        self._set_spacing(Elements.A_SPC_BEF, value)

    @property
    def space_after(self) -> float:
        """Returns or sets the amount of space after the last line in a paragraph with no inheritance. A positive value specifies the percentage of the font size that the white space should be. A negative value specifies the size of the white space in point size. Read/write ."""
        return self._get_spacing(Elements.A_SPC_AFT)

    @space_after.setter
    def space_after(self, value: float):
        self._set_spacing(Elements.A_SPC_AFT, value)

    # --- NullableBool properties ---

    @property
    def east_asian_line_break(self) -> NullableBool:
        """Determines whether the East Asian line break is used in a paragraph. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('eaLnBrk')

    @east_asian_line_break.setter
    def east_asian_line_break(self, value: NullableBool):
        self._set_nullable_bool_attr('eaLnBrk', value)

    @property
    def right_to_left(self) -> NullableBool:
        """Determines whether the Right to Left writing is used in a paragraph. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('rtl')

    @right_to_left.setter
    def right_to_left(self, value: NullableBool):
        self._set_nullable_bool_attr('rtl', value)

    @property
    def latin_line_break(self) -> NullableBool:
        """Determines whether the Latin line break is used in a paragraph. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('latinLnBrk')

    @latin_line_break.setter
    def latin_line_break(self, value: NullableBool):
        self._set_nullable_bool_attr('latinLnBrk', value)

    @property
    def hanging_punctuation(self) -> NullableBool:
        """Determines whether the hanging punctuation is used in a paragraph. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('hangingPunct')

    @hanging_punctuation.setter
    def hanging_punctuation(self, value: NullableBool):
        self._set_nullable_bool_attr('hangingPunct', value)

    # --- EMU-based float properties (NaN = undefined) ---

    def _get_emu_attr(self, attr):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return float('nan')
        val = self._ppr_element.get(attr)
        if val is None:
            return float('nan')
        return int(val) / EMU_PER_POINT

    def _set_emu_attr(self, attr, value):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if math.isnan(value):
            if attr in self._ppr_element.attrib:
                del self._ppr_element.attrib[attr]
        else:
            self._ppr_element.set(attr, str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin in a paragraph with no inheritance. Read/write ."""
        return self._get_emu_attr('marL')

    @margin_left.setter
    def margin_left(self, value: float):
        self._set_emu_attr('marL', value)

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin in a paragraph with no inheritance. Read/write ."""
        return self._get_emu_attr('marR')

    @margin_right.setter
    def margin_right(self, value: float):
        self._set_emu_attr('marR', value)

    @property
    def indent(self) -> float:
        """Returns or sets paragraph First Line Indent/Hanging Indent with no inheritance. Hanging Indent can be defined with negative values. Read/write ."""
        return self._get_emu_attr('indent')

    @indent.setter
    def indent(self, value: float):
        self._set_emu_attr('indent', value)

    @property
    def default_tab_size(self) -> float:
        """Returns or sets default tabulation size with no inheritance. Read/write ."""
        return self._get_emu_attr('defTabSz')

    @default_tab_size.setter
    def default_tab_size(self, value: float):
        self._set_emu_attr('defTabSz', value)

    # --- Tabs (read-only) ---


    # --- Font alignment ---

    @property
    def font_alignment(self) -> FontAlignment:
        """Returns or sets a font alignment in a paragraph with no inheritance. Read/write ."""
        from .FontAlignment import FontAlignment
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return FontAlignment.DEFAULT
        val = self._ppr_element.get('fontAlgn')
        if val is None:
            return FontAlignment.DEFAULT
        name = _FONT_ALIGN_MAP.get(val)
        return FontAlignment[name] if name else FontAlignment.DEFAULT

    @font_alignment.setter
    def font_alignment(self, value: FontAlignment):
        from .FontAlignment import FontAlignment
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == FontAlignment.DEFAULT:
            if 'fontAlgn' in self._ppr_element.attrib:
                del self._ppr_element.attrib['fontAlgn']
        else:
            ooxml_val = _FONT_ALIGN_MAP_REV.get(value.name)
            if ooxml_val:
                self._ppr_element.set('fontAlgn', ooxml_val)
        self._save()

    # --- Bullet (read-only) ---

    @property
    def bullet(self) -> IBulletFormat:
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        from .BulletFormat import BulletFormat
        bf = BulletFormat()
        bf._init_internal(self._ppr_element, self._slide_part, self._parent_slide)
        return bf

    # --- Depth ---

    @property
    def depth(self) -> int:
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return 0
        val = self._ppr_element.get('lvl')
        if val is None:
            return 0
        return int(val)

    @depth.setter
    def depth(self, value: int):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == 0:
            if 'lvl' in self._ppr_element.attrib:
                del self._ppr_element.attrib['lvl']
        else:
            self._ppr_element.set('lvl', str(value))
        self._save()

    # --- Default portion format (read-only) ---

    @property
    def default_portion_format(self) -> IPortionFormat:
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        def_rpr = self._ppr_element.find(Elements.A_DEF_R_PR)
        if def_rpr is None:
            def_rpr = _ppr_insert_child(self._ppr_element, Elements.A_DEF_R_PR)
        from .PortionFormat import PortionFormat
        pf = PortionFormat()
        pf._init_internal(def_rpr, self._slide_part, self._parent_slide)
        return pf

