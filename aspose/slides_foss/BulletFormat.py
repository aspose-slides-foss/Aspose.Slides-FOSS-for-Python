from __future__ import annotations
import math
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IBulletFormat import IBulletFormat
from ._internal.pptx.constants import NS, Elements
from .ParagraphFormat import _ppr_insert_child

if TYPE_CHECKING:
    from .BulletType import BulletType
    from .IBulletFormatEffectiveData import IBulletFormatEffectiveData
    from .IColorFormat import IColorFormat
    from .IFontData import IFontData
    from .ISlidesPicture import ISlidesPicture
    from .NullableBool import NullableBool
    from .NumberedBulletStyle import NumberedBulletStyle

# OOXML buAutoNum type -> NumberedBulletStyle enum name
_AUTO_NUM_MAP = {
    'alphaLcParenBoth': 'BULLET_ALPHA_LC_PAREN_BOTH',
    'alphaLcParenR': 'BULLET_ALPHA_LC_PAREN_RIGHT',
    'alphaLcPeriod': 'BULLET_ALPHA_LC_PERIOD',
    'alphaUcParenBoth': 'BULLET_ALPHA_UC_PAREN_BOTH',
    'alphaUcParenR': 'BULLET_ALPHA_UC_PAREN_RIGHT',
    'alphaUcPeriod': 'BULLET_ALPHA_UC_PERIOD',
    'arabicParenBoth': 'BULLET_ARABIC_PAREN_BOTH',
    'arabicParenR': 'BULLET_ARABIC_PAREN_RIGHT',
    'arabicPeriod': 'BULLET_ARABIC_PERIOD',
    'arabicPlain': 'BULLET_ARABIC_PLAIN',
    'romanLcParenBoth': 'BULLET_ROMAN_LC_PAREN_BOTH',
    'romanLcParenR': 'BULLET_ROMAN_LC_PAREN_RIGHT',
    'romanLcPeriod': 'BULLET_ROMAN_LC_PERIOD',
    'romanUcParenBoth': 'BULLET_ROMAN_UC_PAREN_BOTH',
    'romanUcParenR': 'BULLET_ROMAN_UC_PAREN_RIGHT',
    'romanUcPeriod': 'BULLET_ROMAN_UC_PERIOD',
    'circleNumDbPlain': 'BULLET_CIRCLE_NUM_DB_PLAIN',
    'circleNumWdBlackPlain': 'BULLET_CIRCLE_NUM_WD_BLACK_PLAIN',
    'circleNumWdWhitePlain': 'BULLET_CIRCLE_NUM_WD_WHITE_PLAIN',
    'ea1ChsPeriod': 'BULLET_SIMP_CHIN_PERIOD',
    'ea1ChsPlain': 'BULLET_SIMP_CHIN_PLAIN',
    'ea1ChtPeriod': 'BULLET_TRAD_CHIN_PERIOD',
    'ea1ChtPlain': 'BULLET_TRAD_CHIN_PLAIN',
    'ea1JpnChsDbPeriod': 'BULLET_KANJI_SIMP_CHIN_DB_PERIOD',
    'ea1JpnKorPeriod': 'BULLET_KANJI_KOREAN_PERIOD',
    'ea1JpnKorPlain': 'BULLET_KANJI_KOREAN_PLAIN',
    'arabic1Minus': 'BULLET_ARABIC_ALPHA_DASH',
    'arabic2Minus': 'BULLET_ARABIC_ABJAD_DASH',
    'hebrew2Minus': 'BULLET_HEBREW_ALPHA_DASH',
    'thaiAlphaPeriod': 'BULLET_THAI_ALPHA_PERIOD',
    'thaiAlphaParenR': 'BULLET_THAI_ALPHA_PAREN_RIGHT',
    'thaiAlphaParenBoth': 'BULLET_THAI_ALPHA_PAREN_BOTH',
    'thaiNumPeriod': 'BULLET_THAI_NUM_PERIOD',
    'thaiNumParenR': 'BULLET_THAI_NUM_PAREN_RIGHT',
    'thaiNumParenBoth': 'BULLET_THAI_NUM_PAREN_BOTH',
    'hindiAlphaPeriod': 'BULLET_HINDI_ALPHA_PERIOD',
    'hindiNumPeriod': 'BULLET_HINDI_NUM_PERIOD',
    'hindiNumParenR': 'BULLET_HINDI_NUM_PAREN_RIGHT',
    'hindiAlpha1Period': 'BULLET_HINDI_ALPHA_1_PERIOD',
    'arabicDbPeriod': 'BULLET_ARABIC_DB_PERIOD',
    'arabicDbPlain': 'BULLET_ARABIC_DB_PLAIN',
}
_AUTO_NUM_MAP_REV = {v: k for k, v in _AUTO_NUM_MAP.items()}

# Bullet type element tags (mutually exclusive in pPr)
_BULLET_TYPE_TAGS = (
    Elements.A_BU_NONE,
    Elements.A_BU_CHAR,
    Elements.A_BU_AUTO_NUM,
    Elements.A_BU_BLIP,
)


class BulletFormat(PVIObject, ISlideComponent, IPresentationComponent, IBulletFormat):
    """Represents paragraph bullet formatting properties."""

    def _init_internal(self, ppr_element, slide_part, parent_slide):
        self._ppr_element = ppr_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    def _save(self):
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    def _remove_bullet_type_elements(self):
        """Remove all bullet type elements from pPr."""
        for tag in _BULLET_TYPE_TAGS:
            el = self._ppr_element.find(tag)
            if el is not None:
                self._ppr_element.remove(el)

    # --- type ---

    @property
    def type(self) -> BulletType:
        """Returns or sets the bullet type of a paragraph with no inheritance. Read/write ."""
        from .BulletType import BulletType
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return BulletType.NOT_DEFINED
        if self._ppr_element.find(Elements.A_BU_NONE) is not None:
            return BulletType.NONE
        if self._ppr_element.find(Elements.A_BU_CHAR) is not None:
            return BulletType.SYMBOL
        if self._ppr_element.find(Elements.A_BU_AUTO_NUM) is not None:
            return BulletType.NUMBERED
        if self._ppr_element.find(Elements.A_BU_BLIP) is not None:
            return BulletType.PICTURE
        return BulletType.NOT_DEFINED

    @type.setter
    def type(self, value: BulletType):
        from .BulletType import BulletType
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        self._remove_bullet_type_elements()
        if value == BulletType.NONE:
            _ppr_insert_child(self._ppr_element, Elements.A_BU_NONE)
        elif value == BulletType.SYMBOL:
            _ppr_insert_child(self._ppr_element, Elements.A_BU_CHAR, attrib={'char': '\u2022'})
        elif value == BulletType.NUMBERED:
            _ppr_insert_child(self._ppr_element, Elements.A_BU_AUTO_NUM, attrib={'type': 'arabicPeriod'})
        elif value == BulletType.PICTURE:
            _ppr_insert_child(self._ppr_element, Elements.A_BU_BLIP)
        self._save()

    # --- char ---

    @property
    def char(self) -> str:
        """Returns or sets the bullet char of a paragraph with no inheritance. Read/write ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return ''
        el = self._ppr_element.find(Elements.A_BU_CHAR)
        if el is None:
            return ''
        return el.get('char', '')

    @char.setter
    def char(self, value: str):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        el = self._ppr_element.find(Elements.A_BU_CHAR)
        if el is None:
            self._remove_bullet_type_elements()
            el = _ppr_insert_child(self._ppr_element, Elements.A_BU_CHAR)
        el.set('char', value)
        self._save()

    # --- font ---

    @property
    def font(self) -> IFontData:
        """Returns or sets the bullet font of a paragraph with no inheritance. Read/write ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return None
        el = self._ppr_element.find(Elements.A_BU_FONT)
        if el is None:
            return None
        typeface = el.get('typeface')
        if typeface is None:
            return None
        from .FontData import FontData
        return FontData(typeface)

    @font.setter
    def font(self, value: IFontData):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        el = self._ppr_element.find(Elements.A_BU_FONT)
        if value is None:
            if el is not None:
                self._ppr_element.remove(el)
        else:
            if el is None:
                el = _ppr_insert_child(self._ppr_element, Elements.A_BU_FONT)
            el.set('typeface', value.font_name)
        self._save()

    # --- height ---

    @property
    def height(self) -> float:
        """Returns or sets the bullet height of a paragraph with no inheritance. Value float.NaN determines that bullet inherits height from the first portion in the paragraph. Read/write ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return float('nan')
        pct = self._ppr_element.find(Elements.A_BU_SZ_PCT)
        if pct is not None:
            val = pct.get('val')
            if val is not None:
                return int(val) / 1000.0
        pts = self._ppr_element.find(Elements.A_BU_SZ_PTS)
        if pts is not None:
            val = pts.get('val')
            if val is not None:
                return int(val) / 100.0
        return float('nan')

    @height.setter
    def height(self, value: float):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        # Remove existing size elements
        for tag in (Elements.A_BU_SZ_PCT, Elements.A_BU_SZ_PTS, Elements.A_BU_SZ_TX):
            el = self._ppr_element.find(tag)
            if el is not None:
                self._ppr_element.remove(el)
        if not math.isnan(value):
            # Store as percentage (thousandths of percent)
            _ppr_insert_child(self._ppr_element, Elements.A_BU_SZ_PCT,
                             attrib={'val': str(int(round(value * 1000)))})
        self._save()

    # --- color (read-only sub-object) ---

    @property
    def color(self) -> IColorFormat:
        """Returns the color format of a bullet of a paragraph with no inheritance. Read-only ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        bu_clr = self._ppr_element.find(Elements.A_BU_CLR)
        if bu_clr is None:
            bu_clr = _ppr_insert_child(self._ppr_element, Elements.A_BU_CLR)
        from .ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(bu_clr, self._slide_part, self._parent_slide)
        return cf

    # --- numbered_bullet_start_with ---

    @property
    def numbered_bullet_start_with(self) -> int:
        """Returns or sets the first number which is used for group of numbered bullets with no inheritance. Read/write ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return 1
        el = self._ppr_element.find(Elements.A_BU_AUTO_NUM)
        if el is None:
            return 1
        val = el.get('startAt')
        if val is None:
            return 1
        return int(val)

    @numbered_bullet_start_with.setter
    def numbered_bullet_start_with(self, value: int):
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        el = self._ppr_element.find(Elements.A_BU_AUTO_NUM)
        if el is None:
            self._remove_bullet_type_elements()
            el = _ppr_insert_child(self._ppr_element, Elements.A_BU_AUTO_NUM,
                                   attrib={'type': 'arabicPeriod'})
        if value <= 1:
            if 'startAt' in el.attrib:
                del el.attrib['startAt']
        else:
            el.set('startAt', str(value))
        self._save()

    # --- numbered_bullet_style ---

    @property
    def numbered_bullet_style(self) -> NumberedBulletStyle:
        """Returns or sets the style of a numbered bullet with no inheritance. Read/write ."""
        from .NumberedBulletStyle import NumberedBulletStyle
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return NumberedBulletStyle.NOT_DEFINED
        el = self._ppr_element.find(Elements.A_BU_AUTO_NUM)
        if el is None:
            return NumberedBulletStyle.NOT_DEFINED
        val = el.get('type')
        if val is None:
            return NumberedBulletStyle.NOT_DEFINED
        name = _AUTO_NUM_MAP.get(val)
        return NumberedBulletStyle[name] if name else NumberedBulletStyle.NOT_DEFINED

    @numbered_bullet_style.setter
    def numbered_bullet_style(self, value: NumberedBulletStyle):
        from .NumberedBulletStyle import NumberedBulletStyle
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        el = self._ppr_element.find(Elements.A_BU_AUTO_NUM)
        if value == NumberedBulletStyle.NOT_DEFINED:
            if el is not None:
                self._ppr_element.remove(el)
            return
        if el is None:
            self._remove_bullet_type_elements()
            el = _ppr_insert_child(self._ppr_element, Elements.A_BU_AUTO_NUM)
        ooxml_val = _AUTO_NUM_MAP_REV.get(value.name)
        if ooxml_val:
            el.set('type', ooxml_val)
        self._save()

    # --- is_bullet_hard_color ---

    @property
    def is_bullet_hard_color(self) -> NullableBool:
        """Determines whether the bullet has own color or inherits it from the first portion in the paragraph. NullableBool.True if bullet has own color and NullableBool.False if bullet inherits color from the first portion in the paragraph. Read/write ."""
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return NullableBool.NOT_DEFINED
        if self._ppr_element.find(Elements.A_BU_CLR) is not None:
            return NullableBool.TRUE
        if self._ppr_element.find(Elements.A_BU_CLR_TX) is not None:
            return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @is_bullet_hard_color.setter
    def is_bullet_hard_color(self, value: NullableBool):
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == NullableBool.TRUE:
            # Remove buClrTx; keep existing buClr (preserves color data)
            el = self._ppr_element.find(Elements.A_BU_CLR_TX)
            if el is not None:
                self._ppr_element.remove(el)
            if self._ppr_element.find(Elements.A_BU_CLR) is None:
                _ppr_insert_child(self._ppr_element, Elements.A_BU_CLR)
        elif value == NullableBool.FALSE:
            el = self._ppr_element.find(Elements.A_BU_CLR)
            if el is not None:
                self._ppr_element.remove(el)
            if self._ppr_element.find(Elements.A_BU_CLR_TX) is None:
                _ppr_insert_child(self._ppr_element, Elements.A_BU_CLR_TX)
        else:
            for tag in (Elements.A_BU_CLR, Elements.A_BU_CLR_TX):
                el = self._ppr_element.find(tag)
                if el is not None:
                    self._ppr_element.remove(el)
        self._save()

    # --- is_bullet_hard_font ---

    @property
    def is_bullet_hard_font(self) -> NullableBool:
        """Determines whether the bullet has own font or inherits it from the first portion in the paragraph. NullableBool.True if bullet has own font and NullableBool.False if bullet inherits font from the first portion in the paragraph. Read/write ."""
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return NullableBool.NOT_DEFINED
        if self._ppr_element.find(Elements.A_BU_FONT) is not None:
            return NullableBool.TRUE
        if self._ppr_element.find(Elements.A_BU_FONT_TX) is not None:
            return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @is_bullet_hard_font.setter
    def is_bullet_hard_font(self, value: NullableBool):
        from .NullableBool import NullableBool
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            return
        if value == NullableBool.TRUE:
            # Remove buFontTx; keep existing buFont (preserves font data)
            el = self._ppr_element.find(Elements.A_BU_FONT_TX)
            if el is not None:
                self._ppr_element.remove(el)
            if self._ppr_element.find(Elements.A_BU_FONT) is None:
                _ppr_insert_child(self._ppr_element, Elements.A_BU_FONT)
        elif value == NullableBool.FALSE:
            el = self._ppr_element.find(Elements.A_BU_FONT)
            if el is not None:
                self._ppr_element.remove(el)
            if self._ppr_element.find(Elements.A_BU_FONT_TX) is None:
                _ppr_insert_child(self._ppr_element, Elements.A_BU_FONT_TX)
        else:
            for tag in (Elements.A_BU_FONT, Elements.A_BU_FONT_TX):
                el = self._ppr_element.find(tag)
                if el is not None:
                    self._ppr_element.remove(el)
        self._save()

    # --- picture (read-only) ---

    @property
    def picture(self) -> ISlidesPicture:
        """Returns the picture used as a bullet in a paragraph with no inheritance. Read-only ."""
        if not hasattr(self, '_ppr_element') or self._ppr_element is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        bu_blip = self._ppr_element.find(Elements.A_BU_BLIP)
        if bu_blip is None:
            bu_blip = _ppr_insert_child(self._ppr_element, Elements.A_BU_BLIP)
        blip = bu_blip.find(f'{NS.A}blip')
        if blip is None:
            blip = ET.SubElement(bu_blip, f'{NS.A}blip')
        from .Picture import Picture
        pic = Picture()
        pic._init_internal(blip, self._slide_part, self._parent_slide)
        return pic

    # --- methods ---


