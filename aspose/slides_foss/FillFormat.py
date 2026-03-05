from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IFillFormat import IFillFormat
from .IFillParamSource import IFillParamSource
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .FillType import FillType
    from .IColorFormat import IColorFormat
    from .IGradientFormat import IGradientFormat
    from .IPatternFormat import IPatternFormat
    from .IPictureFillFormat import IPictureFillFormat
    from .NullableBool import NullableBool
    from ._internal.pptx.slide_part import SlidePart

# Fill element tags in the order OOXML expects
_FILL_TAGS = {
    Elements.A_NO_FILL, Elements.A_SOLID_FILL, Elements.A_GRAD_FILL,
    Elements.A_BLIP_FILL, Elements.A_PATT_FILL, Elements.A_GRP_FILL,
}


class FillFormat(PVIObject, ISlideComponent, IPresentationComponent, IFillFormat, IFillParamSource):
    """Represents a fill formatting options."""

    def _init_internal(self, parent_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            parent_element: Any XML element that contains fill children
                (e.g., <p:spPr>, <p:bgPr>, <a:tcPr>, <a:rPr>).
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
        """
        self._parent_element = parent_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _find_fill_element(self) -> ET._Element | None:
        """Find the first fill child element in the parent."""
        for child in self._parent_element:
            if child.tag in _FILL_TAGS:
                return child
        return None

    def _remove_fill_elements(self) -> None:
        """Remove all existing fill child elements from parent."""
        for child in list(self._parent_element):
            if child.tag in _FILL_TAGS:
                self._parent_element.remove(child)

    def _insert_fill_element(self, tag: str) -> ET._Element:
        """Insert a fill element at the correct position in the parent.

        OOXML requires spPr children in order: xfrm, geometry, fill, ln, effects.
        Fill elements must be inserted before <a:ln> and after geometry.
        """
        el = ET.Element(tag)
        # Find the insertion point: before <a:ln> or other post-fill elements
        insert_before = None
        for child in self._parent_element:
            if child.tag in (Elements.A_LN, f"{NS.A}effectLst", f"{NS.A}effectDag",
                             f"{NS.A}scene3d", f"{NS.A}sp3d", f"{NS.A}extLst"):
                insert_before = child
                break
        if insert_before is not None:
            idx = list(self._parent_element).index(insert_before)
            self._parent_element.insert(idx, el)
        else:
            self._parent_element.append(el)
        return el

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def fill_type(self) -> FillType:
        """Returns or sets the type of filling. Read/write."""
        from .FillType import FillType
        el = self._find_fill_element()
        if el is None:
            return FillType.NOT_DEFINED
        tag = el.tag
        if tag == Elements.A_NO_FILL:
            return FillType.NO_FILL
        if tag == Elements.A_SOLID_FILL:
            return FillType.SOLID
        if tag == Elements.A_GRAD_FILL:
            return FillType.GRADIENT
        if tag == Elements.A_PATT_FILL:
            return FillType.PATTERN
        if tag == Elements.A_BLIP_FILL:
            return FillType.PICTURE
        if tag == Elements.A_GRP_FILL:
            return FillType.GROUP
        return FillType.NOT_DEFINED

    @fill_type.setter
    def fill_type(self, value: FillType):
        from .FillType import FillType
        tag_map = {
            FillType.NO_FILL: Elements.A_NO_FILL,
            FillType.SOLID: Elements.A_SOLID_FILL,
            FillType.GRADIENT: Elements.A_GRAD_FILL,
            FillType.PATTERN: Elements.A_PATT_FILL,
            FillType.PICTURE: Elements.A_BLIP_FILL,
            FillType.GROUP: Elements.A_GRP_FILL,
        }
        tag = tag_map.get(value)
        # If the fill type already matches, preserve existing element and children
        existing = self._find_fill_element()
        if existing is not None and tag is not None and existing.tag == tag:
            return
        self._remove_fill_elements()
        if tag is not None:
            el = self._insert_fill_element(tag)
            # Add default linear direction for gradient fills
            if tag == Elements.A_GRAD_FILL:
                ET.SubElement(el, Elements.A_LIN, ang='0', scaled='1')
            # Add default blip and stretch for picture fills
            elif tag == Elements.A_BLIP_FILL:
                ET.SubElement(el, f"{NS.A}blip")
                stretch = ET.SubElement(el, f"{NS.A}stretch")
                ET.SubElement(stretch, f"{NS.A}fillRect")
        self._save()

    def _get_or_create_fill(self, tag: str) -> ET._Element:
        """Get existing fill element of given tag, or create it (removing others)."""
        el = self._find_fill_element()
        if el is not None and el.tag == tag:
            return el
        self._remove_fill_elements()
        el = self._insert_fill_element(tag)
        # Add default linear direction for gradient fills so PowerPoint renders them
        if tag == Elements.A_GRAD_FILL:
            ET.SubElement(el, Elements.A_LIN, ang='0', scaled='1')
        # Add default blip and stretch for picture fills
        elif tag == Elements.A_BLIP_FILL:
            ET.SubElement(el, f"{NS.A}blip")
            stretch = ET.SubElement(el, f"{NS.A}stretch")
            ET.SubElement(stretch, f"{NS.A}fillRect")
        return el

    @property
    def solid_fill_color(self) -> IColorFormat:
        """Returns the fill color. Read-only."""
        from .ColorFormat import ColorFormat
        solid_fill = self._get_or_create_fill(Elements.A_SOLID_FILL)
        cf = ColorFormat()
        cf._init_internal(solid_fill, self._slide_part, self._parent_slide)
        return cf

    @property
    def gradient_format(self) -> IGradientFormat:
        """Returns the gradient fill format. Read-only."""
        from .GradientFormat import GradientFormat
        grad_fill = self._find_fill_element()
        if grad_fill is None or grad_fill.tag != Elements.A_GRAD_FILL:
            grad_fill = self._get_or_create_fill(Elements.A_GRAD_FILL)
        gf = GradientFormat()
        gf._init_internal(grad_fill, self._slide_part, self._parent_slide)
        return gf

    @property
    def pattern_format(self) -> IPatternFormat:
        """Returns the pattern fill format. Read-only."""
        from .PatternFormat import PatternFormat
        patt_fill = self._find_fill_element()
        if patt_fill is None or patt_fill.tag != Elements.A_PATT_FILL:
            patt_fill = self._get_or_create_fill(Elements.A_PATT_FILL)
        pf = PatternFormat()
        pf._init_internal(patt_fill, self._slide_part, self._parent_slide)
        return pf

    @property
    def picture_fill_format(self) -> IPictureFillFormat:
        """Returns the picture fill format. Read-only."""
        from .PictureFillFormat import PictureFillFormat
        blip_fill = self._find_fill_element()
        if blip_fill is None or blip_fill.tag != Elements.A_BLIP_FILL:
            blip_fill = self._get_or_create_fill(Elements.A_BLIP_FILL)
        pff = PictureFillFormat()
        pff._init_internal(blip_fill, self._slide_part, self._parent_slide)
        return pff

    @property
    def rotate_with_shape(self) -> NullableBool:
        """Determines whether the fill should be rotated with shape. Read/write."""
        from .NullableBool import NullableBool
        el = self._find_fill_element()
        if el is None:
            return NullableBool.NOT_DEFINED
        val = el.get('rotWithShape')
        if val is None:
            return NullableBool.NOT_DEFINED
        return NullableBool.TRUE if val == '1' else NullableBool.FALSE

    @rotate_with_shape.setter
    def rotate_with_shape(self, value: NullableBool):
        from .NullableBool import NullableBool
        el = self._find_fill_element()
        if el is None:
            return
        if value == NullableBool.NOT_DEFINED:
            if 'rotWithShape' in el.attrib:
                del el.attrib['rotWithShape']
        else:
            el.set('rotWithShape', '1' if value == NullableBool.TRUE else '0')
        self._save()


