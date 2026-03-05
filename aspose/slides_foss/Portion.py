from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .IPortion import IPortion
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .IPortionFormat import IPortionFormat
    from .IPresentation import IPresentation

class Portion(IPortion, ISlideComponent, IPresentationComponent):
    """Represents a portion of text inside a text paragraph."""



    def __init__(self, *args, **kwargs):
        import lxml.etree as ET
        from ._internal.pptx.constants import Elements
        self._p_element = None
        self._txbody_element = None
        self._slide_part = None
        self._parent_slide = None
        # Always create a valid <a:r> element
        self._r_element = ET.Element(Elements.A_R)
        t_elem = ET.SubElement(self._r_element, Elements.A_T)
        if len(args) == 1 and isinstance(args[0], str):
            t_elem.text = args[0]
        else:
            t_elem.text = ''

    def _init_internal(self, r_element, p_element, txbody_element, slide_part, parent_slide):
        self._r_element = r_element
        self._p_element = p_element
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    @property
    def portion_format(self) -> IPortionFormat:
        """Returns oformatting bject which contains explicitly set formatting properties of the text portion with no inheritance applied. Read-only ."""
        if self._r_element is None:
            return None
        from ._internal.pptx.constants import Elements
        from .PortionFormat import PortionFormat
        rpr = self._r_element.find(Elements.A_R_PR)
        if rpr is None:
            import lxml.etree as ET
            rpr = ET.Element(Elements.A_R_PR)
            self._r_element.insert(0, rpr)
        pf = PortionFormat()
        slide_part = getattr(self, '_slide_part', None)
        parent_slide = getattr(self, '_parent_slide', None)
        pf._init_internal(rpr, slide_part, parent_slide)
        return pf

    @property
    def text(self) -> str:
        """Gets or sets the plain text of a portion. Read/write ."""
        if self._r_element is None:
            return ''
        from ._internal.pptx.constants import Elements
        t_elem = self._r_element.find(Elements.A_T)
        if t_elem is None:
            return ''
        return t_elem.text or ''

    @text.setter
    def text(self, value: str):
        if self._r_element is None:
            return
        from ._internal.pptx.constants import Elements
        import lxml.etree as ET
        t_elem = self._r_element.find(Elements.A_T)
        if t_elem is None:
            t_elem = ET.SubElement(self._r_element, Elements.A_T)
        t_elem.text = value
        if self._slide_part:
            self._slide_part.save()


    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def slide(self) -> IBaseSlide:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide
        return None

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def presentation(self) -> IPresentation:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        return None






