from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ITextFrameFormat import ITextFrameFormat
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT, ROTATION_UNIT

if TYPE_CHECKING:
    from .IThreeDFormat import IThreeDFormat
    from .NullableBool import NullableBool
    from .TextAnchorType import TextAnchorType
    from .TextAutofitType import TextAutofitType
    from .TextShapeType import TextShapeType
    from .TextVerticalType import TextVerticalType
    from .IBaseSlide import IBaseSlide
    from .IPresentation import IPresentation
    from ._internal.pptx.slide_part import SlidePart

# OOXML anchor value → TextAnchorType enum name
_ANCHOR_MAP = {
    't': 'TOP', 'ctr': 'CENTER', 'b': 'BOTTOM',
    'just': 'JUSTIFIED', 'dist': 'DISTRIBUTED',
}
_ANCHOR_MAP_REV = {v: k for k, v in _ANCHOR_MAP.items()}

# OOXML vert value → TextVerticalType enum name
_VERT_MAP = {
    'horz': 'HORIZONTAL', 'vert': 'VERTICAL', 'vert270': 'VERTICAL270',
    'wordArtVert': 'WORD_ART_VERTICAL', 'eaVert': 'EAST_ASIAN_VERTICAL',
    'mongolianVert': 'MONGOLIAN_VERTICAL', 'wordArtVertRtl': 'WORD_ART_VERTICAL_RIGHT_TO_LEFT',
}
_VERT_MAP_REV = {v: k for k, v in _VERT_MAP.items()}

# OOXML prstTxWarp prst value → TextShapeType enum name
_WARP_MAP = {
    'textNoShape': 'NONE', 'textPlain': 'PLAIN', 'textStop': 'STOP',
    'textTriangle': 'TRIANGLE', 'textTriangleInverted': 'TRIANGLE_INVERTED',
    'textChevron': 'CHEVRON', 'textChevronInverted': 'CHEVRON_INVERTED',
    'textRingInside': 'RING_INSIDE', 'textRingOutside': 'RING_OUTSIDE',
    'textArchUp': 'ARCH_UP', 'textArchDown': 'ARCH_DOWN',
    'textCircle': 'CIRCLE', 'textButton': 'BUTTON',
    'textArchUpPour': 'ARCH_UP_POUR', 'textArchDownPour': 'ARCH_DOWN_POUR',
    'textCirclePour': 'CIRCLE_POUR', 'textButtonPour': 'BUTTON_POUR',
    'textCurveUp': 'CURVE_UP', 'textCurveDown': 'CURVE_DOWN',
    'textCanUp': 'CAN_UP', 'textCanDown': 'CAN_DOWN',
    'textWave1': 'WAVE1', 'textWave2': 'WAVE2',
    'textDoubleWave1': 'DOUBLE_WAVE1', 'textWave4': 'WAVE4',
    'textInflate': 'INFLATE', 'textDeflate': 'DEFLATE',
    'textInflateBottom': 'INFLATE_BOTTOM', 'textDeflateBottom': 'DEFLATE_BOTTOM',
    'textInflateTop': 'INFLATE_TOP', 'textDeflateTop': 'DEFLATE_TOP',
    'textDeflateInflate': 'DEFLATE_INFLATE',
    'textDeflateInflateDeflate': 'DEFLATE_INFLATE_DEFLATE',
    'textFadeRight': 'FADE_RIGHT', 'textFadeLeft': 'FADE_LEFT',
    'textFadeUp': 'FADE_UP', 'textFadeDown': 'FADE_DOWN',
    'textSlantUp': 'SLANT_UP', 'textSlantDown': 'SLANT_DOWN',
    'textCascadeUp': 'CASCADE_UP', 'textCascadeDown': 'CASCADE_DOWN',
}
_WARP_MAP_REV = {v: k for k, v in _WARP_MAP.items()}


class TextFrameFormat(PVIObject, ISlideComponent, IPresentationComponent, ITextFrameFormat):
    """Contains the TextFrame's formatTextFrameFormatting properties."""
    def __init__(self):
        # Create a detached txBody with bodyPr so the object works standalone
        # (e.g. ``fmt = TextFrameFormat(); fmt.text_vertical_type = ...``).
        # _init_internal() replaces these with the real XML when bound to a shape.
        self._txbody_element = ET.Element(Elements.A_TX_BODY)
        ET.SubElement(self._txbody_element, Elements.A_BODY_PR)
        self._slide_part = None
        self._parent_slide = None

    def _init_internal(self, txbody_element: ET._Element, slide_part: SlidePart, parent_slide) -> TextFrameFormat:
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    def _get_body_pr(self) -> ET._Element | None:
        if self._txbody_element is None:
            return None
        return self._txbody_element.find(Elements.A_BODY_PR)

    def _ensure_body_pr(self) -> ET._Element:
        body_pr = self._get_body_pr()
        if body_pr is not None:
            return body_pr
        body_pr = ET.SubElement(self._txbody_element, Elements.A_BODY_PR)
        return body_pr

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    # --- slide / presentation delegation ---

    @property
    def slide(self) -> IBaseSlide:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide
        return None

    @property
    def presentation(self) -> IPresentation:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        return None

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    # --- Margin properties (EMU ↔ points) ---

    def _get_margin(self, attr: str, default_emu: int = 91440) -> float:
        body_pr = self._get_body_pr()
        if body_pr is None:
            return default_emu / EMU_PER_POINT
        val = body_pr.get(attr)
        if val is None:
            return default_emu / EMU_PER_POINT
        return int(val) / EMU_PER_POINT

    def _set_margin(self, attr: str, value: float) -> None:
        body_pr = self._ensure_body_pr()
        body_pr.set(attr, str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin (points) in a TextFrame. Read/write ."""
        return self._get_margin('lIns')

    @margin_left.setter
    def margin_left(self, value: float):
        self._set_margin('lIns', value)

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin (points) in a TextFrame. Read/write ."""
        return self._get_margin('rIns')

    @margin_right.setter
    def margin_right(self, value: float):
        self._set_margin('rIns', value)

    @property
    def margin_top(self) -> float:
        """Returns or sets the top margin (points) in a TextFrame. Read/write ."""
        return self._get_margin('tIns', 45720)

    @margin_top.setter
    def margin_top(self, value: float):
        self._set_margin('tIns', value)

    @property
    def margin_bottom(self) -> float:
        """Returns or sets the bottom margin (points) in a TextFrame. Read/write ."""
        return self._get_margin('bIns', 45720)

    @margin_bottom.setter
    def margin_bottom(self, value: float):
        self._set_margin('bIns', value)

    # --- wrap_text ---

    @property
    def wrap_text(self) -> NullableBool:
        """True if text is wrapped at TextFrame's margins. Read/write ."""
        from .NullableBool import NullableBool
        body_pr = self._get_body_pr()
        if body_pr is None:
            return NullableBool.NOT_DEFINED
        val = body_pr.get('wrap')
        if val is None:
            return NullableBool.NOT_DEFINED
        if val == 'square':
            return NullableBool.TRUE
        if val == 'none':
            return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @wrap_text.setter
    def wrap_text(self, value: NullableBool):
        from .NullableBool import NullableBool
        body_pr = self._ensure_body_pr()
        if value == NullableBool.TRUE:
            body_pr.set('wrap', 'square')
        elif value == NullableBool.FALSE:
            body_pr.set('wrap', 'none')
        else:
            if 'wrap' in body_pr.attrib:
                del body_pr.attrib['wrap']
        self._save()

    # --- anchoring_type ---

    @property
    def anchoring_type(self) -> TextAnchorType:
        """Returns or sets vertical anchor text in a TextFrame. Read/write ."""
        from .TextAnchorType import TextAnchorType
        body_pr = self._get_body_pr()
        if body_pr is None:
            return TextAnchorType.NOT_DEFINED
        val = body_pr.get('anchor')
        if val is None:
            return TextAnchorType.NOT_DEFINED
        name = _ANCHOR_MAP.get(val)
        return TextAnchorType[name] if name else TextAnchorType.NOT_DEFINED

    @anchoring_type.setter
    def anchoring_type(self, value: TextAnchorType):
        from .TextAnchorType import TextAnchorType
        body_pr = self._ensure_body_pr()
        if value == TextAnchorType.NOT_DEFINED:
            if 'anchor' in body_pr.attrib:
                del body_pr.attrib['anchor']
        else:
            ooxml_val = _ANCHOR_MAP_REV.get(value.name)
            if ooxml_val:
                body_pr.set('anchor', ooxml_val)
        self._save()

    # --- center_text ---

    @property
    def center_text(self) -> NullableBool:
        """If NullableBool.True then text should be centered in box horizontally. Read/write ."""
        from .NullableBool import NullableBool
        body_pr = self._get_body_pr()
        if body_pr is None:
            return NullableBool.NOT_DEFINED
        val = body_pr.get('anchorCtr')
        if val is None:
            return NullableBool.NOT_DEFINED
        return NullableBool.TRUE if val == '1' else NullableBool.FALSE

    @center_text.setter
    def center_text(self, value: NullableBool):
        from .NullableBool import NullableBool
        body_pr = self._ensure_body_pr()
        if value == NullableBool.TRUE:
            body_pr.set('anchorCtr', '1')
        elif value == NullableBool.FALSE:
            body_pr.set('anchorCtr', '0')
        else:
            if 'anchorCtr' in body_pr.attrib:
                del body_pr.attrib['anchorCtr']
        self._save()

    # --- text_vertical_type ---

    @property
    def text_vertical_type(self) -> TextVerticalType:
        """Determines text orientation. Read/write ."""
        from .TextVerticalType import TextVerticalType
        body_pr = self._get_body_pr()
        if body_pr is None:
            return TextVerticalType.NOT_DEFINED
        val = body_pr.get('vert')
        if val is None:
            return TextVerticalType.NOT_DEFINED
        name = _VERT_MAP.get(val)
        return TextVerticalType[name] if name else TextVerticalType.NOT_DEFINED

    @text_vertical_type.setter
    def text_vertical_type(self, value: TextVerticalType):
        from .TextVerticalType import TextVerticalType
        body_pr = self._ensure_body_pr()
        if value == TextVerticalType.NOT_DEFINED:
            if 'vert' in body_pr.attrib:
                del body_pr.attrib['vert']
        else:
            ooxml_val = _VERT_MAP_REV.get(value.name)
            if ooxml_val:
                body_pr.set('vert', ooxml_val)
        self._save()

    # --- autofit_type ---

    @property
    def autofit_type(self) -> TextAutofitType:
        """Returns or sets text's autofit mode. Read/write ."""
        from .TextAutofitType import TextAutofitType
        body_pr = self._get_body_pr()
        if body_pr is None:
            return TextAutofitType.NOT_DEFINED
        if body_pr.find(Elements.A_NO_AUTOFIT) is not None:
            return TextAutofitType.NONE
        if body_pr.find(Elements.A_SP_AUTO_FIT) is not None:
            return TextAutofitType.SHAPE
        if body_pr.find(Elements.A_NORM_AUTOFIT) is not None:
            return TextAutofitType.NORMAL
        return TextAutofitType.NOT_DEFINED

    @autofit_type.setter
    def autofit_type(self, value: TextAutofitType):
        from .TextAutofitType import TextAutofitType
        body_pr = self._ensure_body_pr()
        # Remove existing autofit elements
        for tag in (Elements.A_NO_AUTOFIT, Elements.A_SP_AUTO_FIT, Elements.A_NORM_AUTOFIT):
            existing = body_pr.find(tag)
            if existing is not None:
                body_pr.remove(existing)
        # Add the new one
        if value == TextAutofitType.NONE:
            ET.SubElement(body_pr, Elements.A_NO_AUTOFIT)
        elif value == TextAutofitType.SHAPE:
            ET.SubElement(body_pr, Elements.A_SP_AUTO_FIT)
            self._resize_shape_to_fit_text(body_pr)
        elif value == TextAutofitType.NORMAL:
            ET.SubElement(body_pr, Elements.A_NORM_AUTOFIT)
        self._save()

    def _resize_shape_to_fit_text(self, body_pr) -> None:
        """Resize the parent shape to fit text content, preserving vertical center."""
        txbody = self._txbody_element
        if txbody is None:
            return
        sp_element = txbody.getparent()
        if sp_element is None:
            return
        sp_pr = sp_element.find(Elements.SP_PR)
        if sp_pr is None:
            return
        xfrm = sp_pr.find(f"{NS.A}xfrm")
        if xfrm is None:
            return
        ext = xfrm.find(f"{NS.A}ext")
        off = xfrm.find(f"{NS.A}off")
        if ext is None or off is None:
            return

        # Count paragraphs
        num_paragraphs = max(1, len(txbody.findall(Elements.A_P)))

        # Default font size 18pt, single line spacing = 120% of font size
        default_font_size_emu = int(18.0 * EMU_PER_POINT)
        line_height_emu = int(default_font_size_emu * 1.2)
        text_height_emu = num_paragraphs * line_height_emu

        # Top and bottom margins (default 45720 EMU = 3.6pt each)
        top_margin = int(body_pr.get('tIns', '45720'))
        bottom_margin = int(body_pr.get('bIns', '45720'))
        required_height = text_height_emu + top_margin + bottom_margin

        # Resize preserving vertical center
        current_y = int(off.get('y', '0'))
        current_cy = int(ext.get('cy', '0'))
        center_y = current_y + current_cy // 2
        new_y = center_y - required_height // 2

        ext.set('cy', str(required_height))
        off.set('y', str(new_y))

    # --- column_count ---

    @property
    def column_count(self) -> int:
        """Returns or sets number of columns in the text area. Read/write ."""
        body_pr = self._get_body_pr()
        if body_pr is None:
            return 0
        val = body_pr.get('numCol')
        if val is None:
            return 0
        return max(0, int(val))

    @column_count.setter
    def column_count(self, value: int):
        body_pr = self._ensure_body_pr()
        value = max(0, value)
        if value == 0:
            if 'numCol' in body_pr.attrib:
                del body_pr.attrib['numCol']
        else:
            body_pr.set('numCol', str(value))
        self._save()

    # --- column_spacing ---

    @property
    def column_spacing(self) -> float:
        """Returns or sets the space between text columns (in points). Read/write ."""
        body_pr = self._get_body_pr()
        if body_pr is None:
            return 0.0
        val = body_pr.get('spcCol')
        if val is None:
            return 0.0
        return max(0.0, int(val) / EMU_PER_POINT)

    @column_spacing.setter
    def column_spacing(self, value: float):
        body_pr = self._ensure_body_pr()
        value = max(0.0, value)
        body_pr.set('spcCol', str(int(round(value * EMU_PER_POINT))))
        self._save()

    # --- rotation_angle ---

    @property
    def rotation_angle(self) -> float:
        """Specifies custom the rotation that is being applied to the text within the bounding box. Read/write ."""
        body_pr = self._get_body_pr()
        if body_pr is None:
            return 0.0
        val = body_pr.get('rot')
        if val is None:
            return 0.0
        return int(val) / ROTATION_UNIT

    @rotation_angle.setter
    def rotation_angle(self, value: float):
        body_pr = self._ensure_body_pr()
        body_pr.set('rot', str(int(round(value * ROTATION_UNIT))))
        self._save()

    # --- transform (prstTxWarp) ---

    @property
    def transform(self) -> TextShapeType:
        """Gets or sets text wrapping shape. Read/write ."""
        from .TextShapeType import TextShapeType
        body_pr = self._get_body_pr()
        if body_pr is None:
            return TextShapeType.NOT_DEFINED
        warp = body_pr.find(Elements.A_PRST_TX_WARP)
        if warp is None:
            return TextShapeType.NOT_DEFINED
        prst = warp.get('prst')
        if prst is None:
            return TextShapeType.NOT_DEFINED
        name = _WARP_MAP.get(prst)
        return TextShapeType[name] if name else TextShapeType.NOT_DEFINED

    @transform.setter
    def transform(self, value: TextShapeType):
        from .TextShapeType import TextShapeType
        body_pr = self._ensure_body_pr()
        existing = body_pr.find(Elements.A_PRST_TX_WARP)
        if value == TextShapeType.NOT_DEFINED:
            if existing is not None:
                body_pr.remove(existing)
        else:
            ooxml_val = _WARP_MAP_REV.get(value.name)
            if ooxml_val:
                if existing is None:
                    existing = ET.SubElement(body_pr, Elements.A_PRST_TX_WARP)
                existing.set('prst', ooxml_val)
        self._save()

    # --- keep_text_flat ---

    @property
    def keep_text_flat(self) -> bool:
        """Gets or sets keeping text flat even if a 3-D Rotation effect was applied. Read/write ."""
        body_pr = self._get_body_pr()
        if body_pr is None:
            return False
        return body_pr.get('upright') == '1'

    @keep_text_flat.setter
    def keep_text_flat(self, value: bool):
        body_pr = self._ensure_body_pr()
        if value:
            body_pr.set('upright', '1')
        else:
            if 'upright' in body_pr.attrib:
                del body_pr.attrib['upright']
        self._save()

    # --- three_d_format ---

    @property
    def three_d_format(self) -> IThreeDFormat:
        """Returns the ThreeDFormat object that represents 3d effect properties for a text. Read-only ."""
        from .ThreeDFormat import ThreeDFormat
        body_pr = self._ensure_body_pr()
        fmt = ThreeDFormat()
        fmt._init_internal(body_pr, self._slide_part, self._parent_slide)
        return fmt

    # --- Not yet implemented ---


