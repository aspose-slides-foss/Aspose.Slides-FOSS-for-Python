from __future__ import annotations
from typing import overload, TYPE_CHECKING
from .ITextFrame import ITextFrame
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .ICell import ICell
    from .IParagraphCollection import IParagraphCollection
    from .IPresentation import IPresentation
    from .IShape import IShape
    from .ITextFrameFormat import ITextFrameFormat

class TextFrame(ITextFrame, ISlideComponent, IPresentationComponent):
    """Represents a TextFrame."""

    def _init_internal(self, txbody_element, slide_part, parent_slide, parent_shape=None):
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._parent_shape = parent_shape
        return self

    @property
    def paragraphs(self) -> IParagraphCollection:
        """Returns the list of all paragraphs in a frame. Read-only ."""
        from .ParagraphCollection import ParagraphCollection
        coll = ParagraphCollection()
        coll._init_internal(self._txbody_element, self._slide_part, self._parent_slide)
        return coll

    @property
    def text(self) -> str:
        """Gets or sets the plain text for a TextFrame. Read/write ."""
        if self._txbody_element is None:
            return ''
        from ._internal.pptx.constants import Elements
        parts = []
        for p_elem in self._txbody_element.findall(Elements.A_P):
            p_parts = []
            for r_elem in p_elem.findall(Elements.A_R):
                t_elem = r_elem.find(Elements.A_T)
                if t_elem is not None and t_elem.text:
                    p_parts.append(t_elem.text)
            parts.append(''.join(p_parts))
        return '\n'.join(parts)

    @text.setter
    def text(self, value: str):
        if self._txbody_element is None:
            return
        import lxml.etree as ET
        from ._internal.pptx.constants import Elements
        # Remove all existing paragraphs
        for p_elem in self._txbody_element.findall(Elements.A_P):
            self._txbody_element.remove(p_elem)
        # Split on \r or \n to create separate paragraphs
        import re
        lines = re.split(r'\r\n|\r|\n', value) if value else ['']
        from ._internal.pptx.constants import NS
        for line in lines:
            p_elem = ET.SubElement(self._txbody_element, Elements.A_P)
            r_elem = ET.SubElement(p_elem, Elements.A_R)
            t_elem = ET.SubElement(r_elem, Elements.A_T)
            t_elem.text = line
        if self._slide_part:
            self._slide_part.save()

    @property
    def text_frame_format(self) -> ITextFrameFormat:
        """Returns the formatting object for this TextFrame object. Read-only ."""
        from .TextFrameFormat import TextFrameFormat
        fmt = TextFrameFormat()
        fmt._init_internal(self._txbody_element, self._slide_part, self._parent_slide)
        return fmt


    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide of a TextFrame. Read-only ."""
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide
        return None

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation of a TextFrame. Read-only ."""
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        return None

    @property
    def parent_shape(self) -> IShape:
        """Returns the parent shape or null if the parent object does not implement the IShape interface Read-only ."""
        if hasattr(self, '_parent_shape'):
            return self._parent_shape
        return None

    @property
    def parent_cell(self) -> ICell:
        """Returns the parent cell or null if the parent object does not implement the ICell interface. Read-only ."""
        if hasattr(self, '_parent_cell'):
            return self._parent_cell
        return None

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self











