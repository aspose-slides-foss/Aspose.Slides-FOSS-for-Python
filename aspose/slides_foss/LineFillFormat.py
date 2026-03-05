from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ILineFillFormat import ILineFillFormat
from .IFillParamSource import IFillParamSource
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .FillType import FillType
    from .IColorFormat import IColorFormat
    from .IGradientFormat import IGradientFormat
    from .IPatternFormat import IPatternFormat
    from .NullableBool import NullableBool
    from ._internal.pptx.slide_part import SlidePart

# Fill element tags within <a:ln>
_FILL_TAGS = {
    Elements.A_NO_FILL, Elements.A_SOLID_FILL, Elements.A_GRAD_FILL,
    Elements.A_PATT_FILL,
}


class LineFillFormat(PVIObject, ISlideComponent, IPresentationComponent, ILineFillFormat, IFillParamSource):
    """Represents properties for lines filling."""

    # Tags that must come AFTER fill elements in <a:ln>
    _AFTER_FILL_TAGS = {
        Elements.A_PRST_DASH, Elements.A_CUST_DASH,
        f"{NS.A}round", f"{NS.A}bevel", f"{NS.A}miter",
        f"{NS.A}headEnd", f"{NS.A}tailEnd", f"{NS.A}extLst",
    }

    def _init_internal(self, ln_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._ln_element = ln_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _find_fill_element(self) -> ET._Element | None:
        for child in self._ln_element:
            if child.tag in _FILL_TAGS:
                return child
        return None

    def _remove_fill_elements(self) -> None:
        for child in list(self._ln_element):
            if child.tag in _FILL_TAGS:
                self._ln_element.remove(child)

    def _insert_fill_element(self, tag: str) -> ET._Element:
        """Insert a fill element at the correct position (before dash/join/end elements)."""
        el = ET.Element(tag)
        for i, child in enumerate(self._ln_element):
            if child.tag in self._AFTER_FILL_TAGS:
                self._ln_element.insert(i, el)
                return el
        self._ln_element.append(el)
        return el

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def fill_type(self) -> FillType:
        """Returns or sets the fill type. Read/write."""
        from .FillType import FillType
        el = self._find_fill_element()
        if el is None:
            return FillType.NOT_DEFINED
        if el.tag == Elements.A_NO_FILL:
            return FillType.NO_FILL
        if el.tag == Elements.A_SOLID_FILL:
            return FillType.SOLID
        if el.tag == Elements.A_GRAD_FILL:
            return FillType.GRADIENT
        if el.tag == Elements.A_PATT_FILL:
            return FillType.PATTERN
        return FillType.NOT_DEFINED

    @fill_type.setter
    def fill_type(self, value: FillType):
        from .FillType import FillType
        tag_map = {
            FillType.NO_FILL: Elements.A_NO_FILL,
            FillType.SOLID: Elements.A_SOLID_FILL,
            FillType.GRADIENT: Elements.A_GRAD_FILL,
            FillType.PATTERN: Elements.A_PATT_FILL,
        }
        tag = tag_map.get(value)
        # If the fill type already matches, preserve existing element and children
        existing = self._find_fill_element()
        if existing is not None and tag is not None and existing.tag == tag:
            return
        self._remove_fill_elements()
        if tag is not None:
            self._insert_fill_element(tag)
        self._save()

    @property
    def rotate_with_shape(self) -> NullableBool:
        """Determines whether the fill should be rotated with a shape. Read/write."""
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

    @property
    def solid_fill_color(self) -> IColorFormat:
        """Returns the color of a solid fill. Read-only."""
        from .ColorFormat import ColorFormat
        el = self._find_fill_element()
        if el is None or el.tag != Elements.A_SOLID_FILL:
            self._remove_fill_elements()
            el = self._insert_fill_element(Elements.A_SOLID_FILL)
        cf = ColorFormat()
        cf._init_internal(el, self._slide_part, self._parent_slide)
        return cf

    @property
    def gradient_format(self) -> IGradientFormat:
        """Returns the gradient fill format. Read-only."""
        from .GradientFormat import GradientFormat
        el = self._find_fill_element()
        if el is None or el.tag != Elements.A_GRAD_FILL:
            self._remove_fill_elements()
            el = self._insert_fill_element(Elements.A_GRAD_FILL)
        gf = GradientFormat()
        gf._init_internal(el, self._slide_part, self._parent_slide)
        return gf

    @property
    def pattern_format(self) -> IPatternFormat:
        """Returns the pattern fill format. Read-only."""
        from .PatternFormat import PatternFormat
        el = self._find_fill_element()
        if el is None or el.tag != Elements.A_PATT_FILL:
            self._remove_fill_elements()
            el = self._insert_fill_element(Elements.A_PATT_FILL)
        pf = PatternFormat()
        pf._init_internal(el, self._slide_part, self._parent_slide)
        return pf

