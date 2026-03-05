from __future__ import annotations
import math
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .IBasePortionFormat import IBasePortionFormat
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat
    from .IFontData import IFontData
    from .ILineFormat import ILineFormat
    from .NullableBool import NullableBool
    from .TextCapType import TextCapType
    from .TextStrikethroughType import TextStrikethroughType
    from .TextUnderlineType import TextUnderlineType
    from ._internal.pptx.slide_part import SlidePart

# OOXML underline type attribute values -> TextUnderlineType enum names
_UNDERLINE_MAP = {
    'none': 'NONE', 'words': 'WORDS', 'sng': 'SINGLE', 'dbl': 'DOUBLE',
    'heavy': 'HEAVY', 'dotted': 'DOTTED', 'dottedHeavy': 'HEAVY_DOTTED',
    'dash': 'DASHED', 'dashHeavy': 'HEAVY_DASHED', 'dashLong': 'LONG_DASHED',
    'dashLongHeavy': 'HEAVY_LONG_DASHED', 'dotDash': 'DOT_DASH',
    'dotDashHeavy': 'HEAVY_DOT_DASH', 'dotDotDash': 'DOT_DOT_DASH',
    'dotDotDashHeavy': 'HEAVY_DOT_DOT_DASH', 'wavy': 'WAVY',
    'wavyHeavy': 'HEAVY_WAVY', 'wavyDbl': 'DOUBLE_WAVY',
}
_UNDERLINE_MAP_REV = {v: k for k, v in _UNDERLINE_MAP.items()}

# OOXML cap attribute values -> TextCapType enum names
_CAP_MAP = {'none': 'NONE', 'small': 'SMALL', 'all': 'ALL'}
_CAP_MAP_REV = {v: k for k, v in _CAP_MAP.items()}

# OOXML strike attribute values -> TextStrikethroughType enum names
_STRIKE_MAP = {'noStrike': 'NONE', 'sngStrike': 'SINGLE', 'dblStrike': 'DOUBLE'}
_STRIKE_MAP_REV = {v: k for k, v in _STRIKE_MAP.items()}


class BasePortionFormat(PVIObject, IBasePortionFormat):
    """Common text portion formatting properties."""

    def __init__(self):
        # Create a detached <a:rPr> so the object works standalone.
        self._rpr_element = ET.Element(Elements.A_R_PR)
        self._slide_part = None
        self._parent_slide = None

    def _init_internal(self, rpr_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            rpr_element: The <a:rPr> XML element containing run properties.
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
        """
        self._rpr_element = rpr_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    # --- Helper methods for NullableBool attributes ---

    def _get_nullable_bool_attr(self, attr: str) -> NullableBool:
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return NullableBool.NOT_DEFINED
        val = self._rpr_element.get(attr)
        if val is None:
            return NullableBool.NOT_DEFINED
        return NullableBool.TRUE if val == '1' else NullableBool.FALSE

    def _set_nullable_bool_attr(self, attr: str, value: NullableBool) -> None:
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return
        if value == NullableBool.NOT_DEFINED:
            if attr in self._rpr_element.attrib:
                del self._rpr_element.attrib[attr]
        else:
            self._rpr_element.set(attr, '1' if value == NullableBool.TRUE else '0')
        self._save()

    # --- Helper methods for font elements ---

    def _get_font(self, tag: str) -> IFontData:
        if self._rpr_element is None:
            return None
        el = self._rpr_element.find(tag)
        if el is None:
            return None
        typeface = el.get('typeface')
        if typeface is None:
            return None
        from .FontData import FontData
        return FontData(typeface)

    def _set_font(self, tag: str, value: IFontData) -> None:
        if self._rpr_element is None:
            return
        el = self._rpr_element.find(tag)
        if value is None:
            if el is not None:
                self._rpr_element.remove(el)
        else:
            if el is None:
                el = ET.SubElement(self._rpr_element, tag)
            el.set('typeface', value.font_name)
        self._save()

    # --- Read-only format object properties ---

    @property
    def line_format(self) -> ILineFormat:
        """Returns the LineFormat properties for text outlining. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .LineFormat import LineFormat
        lf = LineFormat()
        lf._init_internal(self._rpr_element, self._slide_part, self._parent_slide)
        return lf

    @property
    def fill_format(self) -> IFillFormat:
        """Returns the text FillFormat properties. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .FillFormat import FillFormat
        ff = FillFormat()
        ff._init_internal(self._rpr_element, self._slide_part, self._parent_slide)
        return ff

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns the text EffectFormat properties. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .EffectFormat import EffectFormat
        ef = EffectFormat()
        ef._init_internal(self._rpr_element, self._slide_part, self._parent_slide)
        return ef

    @property
    def highlight_color(self) -> IColorFormat:
        """Returns the color used to highlight a text. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .ColorFormat import ColorFormat
        highlight_el = self._rpr_element.find(Elements.A_HIGHLIGHT)
        if highlight_el is None:
            highlight_el = ET.SubElement(self._rpr_element, Elements.A_HIGHLIGHT)
        cf = ColorFormat()
        cf._init_internal(highlight_el, self._slide_part, self._parent_slide)
        return cf

    @property
    def underline_line_format(self) -> ILineFormat:
        """Returns the LineFormat properties used to outline underline line. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .LineFormat import LineFormat
        lf = LineFormat()
        lf._init_internal(self._rpr_element, self._slide_part, self._parent_slide, ln_tag=Elements.A_U_LN)
        return lf

    @property
    def underline_fill_format(self) -> IFillFormat:
        """Returns the underline line FillFormat properties. No inheritance applied. Read-only ."""
        if self._rpr_element is None:
            return None
        from .FillFormat import FillFormat
        # <a:uFill> contains fill children, acts as parent for FillFormat
        u_fill_el = self._rpr_element.find(Elements.A_U_FILL)
        if u_fill_el is None:
            u_fill_el = ET.SubElement(self._rpr_element, Elements.A_U_FILL)
        ff = FillFormat()
        ff._init_internal(u_fill_el, self._slide_part, self._parent_slide)
        return ff

    # --- NullableBool attribute properties ---

    @property
    def font_bold(self) -> NullableBool:
        """Determines whether the font is bold. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('b')

    @font_bold.setter
    def font_bold(self, value: NullableBool):
        self._set_nullable_bool_attr('b', value)

    @property
    def font_italic(self) -> NullableBool:
        """Determines whether the font is itallic. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('i')

    @font_italic.setter
    def font_italic(self, value: NullableBool):
        self._set_nullable_bool_attr('i', value)

    @property
    def kumimoji(self) -> NullableBool:
        """Determines whether the numbers should ignore text eastern language-specific vertical text layout. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('kumimoji')

    @kumimoji.setter
    def kumimoji(self, value: NullableBool):
        self._set_nullable_bool_attr('kumimoji', value)

    @property
    def normalise_height(self) -> NullableBool:
        """Determines whether the height of a text should be normalized. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('normalizeH')

    @normalise_height.setter
    def normalise_height(self, value: NullableBool):
        self._set_nullable_bool_attr('normalizeH', value)

    @property
    def proof_disabled(self) -> NullableBool:
        """Determines whether the text shouldn't be proofed. No inheritance applied. Read/write ."""
        return self._get_nullable_bool_attr('noProof')

    @proof_disabled.setter
    def proof_disabled(self, value: NullableBool):
        self._set_nullable_bool_attr('noProof', value)

    # --- Enum attribute properties ---

    @property
    def font_underline(self) -> TextUnderlineType:
        """Returns or sets the text underline type. No inheritance applied. Read/write ."""
        from .TextUnderlineType import TextUnderlineType
        if self._rpr_element is None:
            return TextUnderlineType.NOT_DEFINED
        val = self._rpr_element.get('u')
        if val is None:
            return TextUnderlineType.NOT_DEFINED
        name = _UNDERLINE_MAP.get(val)
        return TextUnderlineType[name] if name else TextUnderlineType.NOT_DEFINED

    @font_underline.setter
    def font_underline(self, value: TextUnderlineType):
        from .TextUnderlineType import TextUnderlineType
        if self._rpr_element is None:
            return
        if value == TextUnderlineType.NOT_DEFINED:
            if 'u' in self._rpr_element.attrib:
                del self._rpr_element.attrib['u']
        else:
            ooxml_val = _UNDERLINE_MAP_REV.get(value.name)
            if ooxml_val:
                self._rpr_element.set('u', ooxml_val)
        self._save()

    @property
    def text_cap_type(self) -> TextCapType:
        """Returns or sets the type of text capitalization. No inheritance applied. Read/write ."""
        from .TextCapType import TextCapType
        if self._rpr_element is None:
            return TextCapType.NOT_DEFINED
        val = self._rpr_element.get('cap')
        if val is None:
            return TextCapType.NOT_DEFINED
        name = _CAP_MAP.get(val)
        return TextCapType[name] if name else TextCapType.NOT_DEFINED

    @text_cap_type.setter
    def text_cap_type(self, value: TextCapType):
        from .TextCapType import TextCapType
        if self._rpr_element is None:
            return
        if value == TextCapType.NOT_DEFINED:
            if 'cap' in self._rpr_element.attrib:
                del self._rpr_element.attrib['cap']
        else:
            ooxml_val = _CAP_MAP_REV.get(value.name)
            if ooxml_val:
                self._rpr_element.set('cap', ooxml_val)
        self._save()

    @property
    def strikethrough_type(self) -> TextStrikethroughType:
        """Returns or sets the strikethrough type of a text. No inheritance applied. Read/write ."""
        from .TextStrikethroughType import TextStrikethroughType
        if self._rpr_element is None:
            return TextStrikethroughType.NOT_DEFINED
        val = self._rpr_element.get('strike')
        if val is None:
            return TextStrikethroughType.NOT_DEFINED
        name = _STRIKE_MAP.get(val)
        return TextStrikethroughType[name] if name else TextStrikethroughType.NOT_DEFINED

    @strikethrough_type.setter
    def strikethrough_type(self, value: TextStrikethroughType):
        from .TextStrikethroughType import TextStrikethroughType
        if self._rpr_element is None:
            return
        if value == TextStrikethroughType.NOT_DEFINED:
            if 'strike' in self._rpr_element.attrib:
                del self._rpr_element.attrib['strike']
        else:
            ooxml_val = _STRIKE_MAP_REV.get(value.name)
            if ooxml_val:
                self._rpr_element.set('strike', ooxml_val)
        self._save()

    # --- Underline hard/soft properties ---

    @property
    def is_hard_underline_line(self) -> NullableBool:
        """Determines whether the underline style has own LineFormat properties or inherits it from the LineFormat properties of the text. Read/write ."""
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return NullableBool.NOT_DEFINED
        if self._rpr_element.find(Elements.A_U_LN) is not None:
            return NullableBool.TRUE
        if self._rpr_element.find(Elements.A_U_LN_TX) is not None:
            return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @is_hard_underline_line.setter
    def is_hard_underline_line(self, value: NullableBool):
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return
        # Remove existing underline line elements
        for tag in (Elements.A_U_LN, Elements.A_U_LN_TX):
            el = self._rpr_element.find(tag)
            if el is not None:
                self._rpr_element.remove(el)
        if value == NullableBool.TRUE:
            ET.SubElement(self._rpr_element, Elements.A_U_LN)
        elif value == NullableBool.FALSE:
            ET.SubElement(self._rpr_element, Elements.A_U_LN_TX)
        self._save()

    @property
    def is_hard_underline_fill(self) -> NullableBool:
        """Determines whether the underline style has own FillFormat properties or inherits it from the FillFormat properties of the text. Read/write ."""
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return NullableBool.NOT_DEFINED
        if self._rpr_element.find(Elements.A_U_FILL) is not None:
            return NullableBool.TRUE
        if self._rpr_element.find(Elements.A_U_FILL_TX) is not None:
            return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @is_hard_underline_fill.setter
    def is_hard_underline_fill(self, value: NullableBool):
        from .NullableBool import NullableBool
        if self._rpr_element is None:
            return
        # Remove existing underline fill elements
        for tag in (Elements.A_U_FILL, Elements.A_U_FILL_TX):
            el = self._rpr_element.find(tag)
            if el is not None:
                self._rpr_element.remove(el)
        if value == NullableBool.TRUE:
            ET.SubElement(self._rpr_element, Elements.A_U_FILL)
        elif value == NullableBool.FALSE:
            ET.SubElement(self._rpr_element, Elements.A_U_FILL_TX)
        self._save()

    # --- Float attribute properties (NaN = undefined) ---

    @property
    def font_height(self) -> float:
        """Returns or sets the font height of a portion. float.NaN means height is undefined and should be inherited from the Master. Read/write ."""
        if self._rpr_element is None:
            return float('nan')
        val = self._rpr_element.get('sz')
        if val is None:
            return float('nan')
        # OOXML stores font size in hundredths of a point
        return int(val) / 100.0

    @font_height.setter
    def font_height(self, value: float):
        if self._rpr_element is None:
            return
        if math.isnan(value):
            if 'sz' in self._rpr_element.attrib:
                del self._rpr_element.attrib['sz']
        else:
            self._rpr_element.set('sz', str(int(round(value * 100))))
        self._save()

    @property
    def escapement(self) -> float:
        """Returns or sets the superscript or subscript text. Value from -100% (subscript) to 100% (superscript). float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        if self._rpr_element is None:
            return float('nan')
        val = self._rpr_element.get('baseline')
        if val is None:
            return float('nan')
        # OOXML stores as thousandths of percent (e.g., 30000 = 30%)
        return int(val) / 1000.0

    @escapement.setter
    def escapement(self, value: float):
        if self._rpr_element is None:
            return
        if math.isnan(value):
            if 'baseline' in self._rpr_element.attrib:
                del self._rpr_element.attrib['baseline']
        else:
            self._rpr_element.set('baseline', str(int(round(value * 1000))))
        self._save()

    @property
    def kerning_minimal_size(self) -> float:
        """Returns or sets the minimal font size, for which kerning should be switched on. float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        if self._rpr_element is None:
            return float('nan')
        val = self._rpr_element.get('kern')
        if val is None:
            return float('nan')
        # OOXML stores in hundredths of a point
        return int(val) / 100.0

    @kerning_minimal_size.setter
    def kerning_minimal_size(self, value: float):
        if self._rpr_element is None:
            return
        if math.isnan(value):
            if 'kern' in self._rpr_element.attrib:
                del self._rpr_element.attrib['kern']
        else:
            self._rpr_element.set('kern', str(int(round(value * 100))))
        self._save()

    @property
    def spacing(self) -> float:
        """Returns or sets the intercharacter spacing increment. float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        if self._rpr_element is None:
            return float('nan')
        val = self._rpr_element.get('spc')
        if val is None:
            return float('nan')
        # OOXML stores in hundredths of a point
        return int(val) / 100.0

    @spacing.setter
    def spacing(self, value: float):
        if self._rpr_element is None:
            return
        if math.isnan(value):
            if 'spc' in self._rpr_element.attrib:
                del self._rpr_element.attrib['spc']
        else:
            self._rpr_element.set('spc', str(int(round(value * 100))))
        self._save()

    # --- Font properties ---

    @property
    def latin_font(self) -> IFontData:
        """Returns or sets the Latin font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        return self._get_font(Elements.A_LATIN)

    @latin_font.setter
    def latin_font(self, value: IFontData):
        self._set_font(Elements.A_LATIN, value)

    @property
    def east_asian_font(self) -> IFontData:
        """Returns or sets the East Asian font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        return self._get_font(Elements.A_EA)

    @east_asian_font.setter
    def east_asian_font(self, value: IFontData):
        self._set_font(Elements.A_EA, value)

    @property
    def complex_script_font(self) -> IFontData:
        """Returns or sets the complex script font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        return self._get_font(Elements.A_CS)

    @complex_script_font.setter
    def complex_script_font(self, value: IFontData):
        self._set_font(Elements.A_CS, value)

    @property
    def symbol_font(self) -> IFontData:
        """Returns or sets the symbolic font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        return self._get_font(Elements.A_SYM)

    @symbol_font.setter
    def symbol_font(self, value: IFontData):
        self._set_font(Elements.A_SYM, value)

    # --- String attribute properties ---

    @property
    def language_id(self) -> str:
        """Returns or sets the Id of a proofing language. Used for checking spelling and grammar. Read/write ."""
        if self._rpr_element is None:
            return None
        return self._rpr_element.get('lang')

    @language_id.setter
    def language_id(self, value: str):
        if self._rpr_element is None:
            return
        if value is None:
            if 'lang' in self._rpr_element.attrib:
                del self._rpr_element.attrib['lang']
        else:
            self._rpr_element.set('lang', value)
        self._save()

    @property
    def alternative_language_id(self) -> str:
        """Returns or sets the Id of an alternative language. Read/write ."""
        if self._rpr_element is None:
            return None
        return self._rpr_element.get('altLang')

    @alternative_language_id.setter
    def alternative_language_id(self, value: str):
        if self._rpr_element is None:
            return
        if value is None:
            if 'altLang' in self._rpr_element.attrib:
                del self._rpr_element.attrib['altLang']
        else:
            self._rpr_element.set('altLang', value)
        self._save()

    # --- spell_check property ---

    @property
    def spell_check(self) -> bool:
        """Gets or sets a value indicating whether spell checking is enabled for the text portion. When this property is set to false, spelling checks for text elements are suppressed. When set to true, spell checking is allowed. Default value is false."""
        if self._rpr_element is None:
            return False
        val = self._rpr_element.get('noProof')
        if val == '1':
            return False
        # If noProof is not set or is '0', spell check is enabled
        return val is not None and val == '0' or self._rpr_element.get('err') is not None

    @spell_check.setter
    def spell_check(self, value: bool):
        if self._rpr_element is None:
            return
        if not value:
            self._rpr_element.set('noProof', '1')
        else:
            if 'noProof' in self._rpr_element.attrib:
                del self._rpr_element.attrib['noProof']
        self._save()
