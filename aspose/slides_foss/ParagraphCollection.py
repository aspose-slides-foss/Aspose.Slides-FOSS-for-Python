from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .IParagraphCollection import IParagraphCollection
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .IPresentation import IPresentation
    from .Paragraph import Paragraph

from ._internal.base_collection import BaseCollection
class ParagraphCollection(BaseCollection, IParagraphCollection, ISlideComponent, IPresentationComponent):
    """Represents a collection of a paragraphs."""

    def _init_internal(self, txbody_element, slide_part, parent_slide):
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    def _get_paragraphs(self):
        from .Paragraph import Paragraph
        from ._internal.pptx.constants import Elements
        if self._txbody_element is None:
            return []
        paragraphs = []
        for p_elem in self._txbody_element.findall(Elements.A_P):
            para = Paragraph()
            para._init_internal(p_elem, self._txbody_element, self._slide_part, self._parent_slide)
            paragraphs.append(para)
        return paragraphs

    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        return len(self._get_paragraphs())

    @property
    def is_read_only(self) -> bool:
        """Gets a value indicating whether the is read-only. Read-only ."""
        return False

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_enumerable(self) -> Any:
        return self

    def __iter__(self):
        return iter(self._get_paragraphs())

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



    def add(self, *args, **kwargs) -> None:
        if self._txbody_element is None:
            return
        value = args[0]
        p_elem = value._p_element
        self._txbody_element.append(p_elem)
        value._init_internal(p_elem, self._txbody_element, self._slide_part, self._parent_slide)
        if self._slide_part:
            self._slide_part.save()



    def insert(self, *args, **kwargs) -> None:
        from ._internal.pptx.constants import Elements
        if self._txbody_element is None:
            return
        index = args[0]
        value = args[1]
        p_elements = self._txbody_element.findall(Elements.A_P)
        p_elem = value._p_element
        if index >= len(p_elements):
            self._txbody_element.append(p_elem)
        else:
            p_elements[index].addprevious(p_elem)
        value._init_internal(p_elem, self._txbody_element, self._slide_part, self._parent_slide)
        if self._slide_part:
            self._slide_part.save()




    def index_of(self, item) -> int:
        paragraphs = self._get_paragraphs()
        for i, p in enumerate(paragraphs):
            if p._p_element is item._p_element:
                return i
        return -1

    def clear(self) -> None:
        from ._internal.pptx.constants import Elements
        if self._txbody_element is None:
            return
        for p_elem in self._txbody_element.findall(Elements.A_P):
            self._txbody_element.remove(p_elem)
        if self._slide_part:
            self._slide_part.save()

    def contains(self, item) -> bool:
        return self.index_of(item) >= 0


    def remove_at(self, index) -> None:
        from ._internal.pptx.constants import Elements
        if self._txbody_element is None:
            return
        p_elements = self._txbody_element.findall(Elements.A_P)
        if 0 <= index < len(p_elements):
            self._txbody_element.remove(p_elements[index])
            if self._slide_part:
                self._slide_part.save()

    def remove(self, item) -> bool:
        from ._internal.pptx.constants import Elements
        if self._txbody_element is None:
            return False
        for p_elem in self._txbody_element.findall(Elements.A_P):
            if p_elem is item._p_element:
                self._txbody_element.remove(p_elem)
                if self._slide_part:
                    self._slide_part.save()
                return True
        return False


    def __getitem__(self, index: int) -> Paragraph:
        paragraphs = self._get_paragraphs()
        return paragraphs[index]
