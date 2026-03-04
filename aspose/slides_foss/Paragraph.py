from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .IParagraph import IParagraph
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .IParagraphFormat import IParagraphFormat
    from .IPortionCollection import IPortionCollection
    from .IPortionFormat import IPortionFormat
    from .IPresentation import IPresentation

class Paragraph(IParagraph, ISlideComponent, IPresentationComponent):
    """Represents a paragraph of text."""


    def __init__(self, *args, **kwargs):
        self._p_element = None
        self._txbody_element = None
        self._slide_part = None
        self._parent_slide = None
        if len(args) == 0:
            import lxml.etree as ET
            from ._internal.pptx.constants import Elements
            self._p_element = ET.Element(Elements.A_P)

    def _init_internal(self, p_element, txbody_element, slide_part, parent_slide):
        self._p_element = p_element
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        if slide_part is not None and parent_slide is not None:
            from .Picture import flush_pending_blip_images
            flush_pending_blip_images(p_element, slide_part, parent_slide)
        return self

    @property
    def portions(self) -> IPortionCollection:
        """Returns the collection of a text portions. Read-only ."""
        from .PortionCollection import PortionCollection
        coll = PortionCollection()
        coll._init_internal(self._p_element, self._txbody_element, self._slide_part, self._parent_slide)
        return coll

    @property
    def paragraph_format(self) -> IParagraphFormat:
        """Returns the formatting object for this paragraph. Read-only ."""
        if not hasattr(self, '_p_element') or self._p_element is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        from .ParagraphFormat import ParagraphFormat
        ppr = self._p_element.find(Elements.A_P_PR)
        if ppr is None:
            import lxml.etree as ET
            ppr = ET.SubElement(self._p_element, Elements.A_P_PR)
            # pPr should be the first child of <a:p>
            self._p_element.insert(0, ppr)
        pf = ParagraphFormat()
        pf._init_internal(ppr, self._slide_part, self._parent_slide)
        return pf

    @property
    def text(self) -> str:
        """Gets or sets the the plain text of a paragraph. Read/write ."""
        if not hasattr(self, '_p_element') or self._p_element is None:
            return ''
        from ._internal.pptx.constants import Elements
        parts = []
        for r_elem in self._p_element.findall(Elements.A_R):
            t_elem = r_elem.find(Elements.A_T)
            if t_elem is not None and t_elem.text:
                parts.append(t_elem.text)
        return ''.join(parts)

    @text.setter
    def text(self, value: str):
        if not hasattr(self, '_p_element') or self._p_element is None:
            return
        import lxml.etree as ET
        from ._internal.pptx.constants import Elements
        # Remove all existing runs
        for r_elem in self._p_element.findall(Elements.A_R):
            self._p_element.remove(r_elem)
        # Create a single new run with the text
        r_elem = ET.SubElement(self._p_element, Elements.A_R)
        t_elem = ET.SubElement(r_elem, Elements.A_T)
        t_elem.text = value
        # Move run before endParaRPr if present
        end_para = self._p_element.find(Elements.A_END_PARA_RPR)
        if end_para is not None:
            end_para.addprevious(r_elem)
        if self._slide_part:
            self._slide_part.save()



    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def slide(self) -> IBaseSlide:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def presentation(self) -> IPresentation:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        raise NotImplementedError("This feature is not yet available in this version.")



