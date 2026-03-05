from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IPortionCollection import IPortionCollection

if TYPE_CHECKING:
    from .Portion import Portion

from ._internal.base_collection import BaseCollection
class PortionCollection(BaseCollection, IPortionCollection):
    """Represents a collection of portions."""

    def _init_internal(self, p_element, txbody_element, slide_part, parent_slide):
        self._p_element = p_element
        self._txbody_element = txbody_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    def _get_portions(self):
        from .Portion import Portion
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return []
        portions = []
        for r_elem in self._p_element.findall(Elements.A_R):
            p = Portion()
            p._init_internal(r_elem, self._p_element, self._txbody_element, self._slide_part, self._parent_slide)
            portions.append(p)
        return portions

    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        return len(self._get_portions())

    @property
    def is_read_only(self) -> bool:
        """Gets a value indicating whether the is read-only. Read-only ."""
        return False

    @property
    def as_i_enumerable(self) -> Any:
        return self

    def __iter__(self):
        return iter(self._get_portions())

    def add(self, value) -> None:
        from .Portion import Portion
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return
        r_elem = value._r_element
        # Insert before endParaRPr if present
        end_para = self._p_element.find(Elements.A_END_PARA_RPR)
        if end_para is not None:
            end_para.addprevious(r_elem)
        else:
            self._p_element.append(r_elem)
        value._init_internal(r_elem, self._p_element, self._txbody_element, self._slide_part, self._parent_slide)
        if self._slide_part:
            self._slide_part.save()

    def index_of(self, item) -> int:
        portions = self._get_portions()
        for i, p in enumerate(portions):
            if p._r_element is item._r_element:
                return i
        return -1

    def insert(self, index, value) -> None:
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return
        r_elements = self._p_element.findall(Elements.A_R)
        r_elem = value._r_element
        if index >= len(r_elements):
            end_para = self._p_element.find(Elements.A_END_PARA_RPR)
            if end_para is not None:
                end_para.addprevious(r_elem)
            else:
                self._p_element.append(r_elem)
        else:
            r_elements[index].addprevious(r_elem)
        value._init_internal(r_elem, self._p_element, self._txbody_element, self._slide_part, self._parent_slide)
        if self._slide_part:
            self._slide_part.save()

    def clear(self) -> None:
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return
        for r_elem in self._p_element.findall(Elements.A_R):
            self._p_element.remove(r_elem)
        if self._slide_part:
            self._slide_part.save()

    def contains(self, item) -> bool:
        return self.index_of(item) >= 0


    def remove(self, item) -> bool:
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return False
        for r_elem in self._p_element.findall(Elements.A_R):
            if r_elem is item._r_element:
                self._p_element.remove(r_elem)
                if self._slide_part:
                    self._slide_part.save()
                return True
        return False

    def remove_at(self, index) -> None:
        from ._internal.pptx.constants import Elements
        if self._p_element is None:
            return
        r_elements = self._p_element.findall(Elements.A_R)
        if 0 <= index < len(r_elements):
            self._p_element.remove(r_elements[index])
            if self._slide_part:
                self._slide_part.save()

    def __getitem__(self, index: int) -> Portion:
        portions = self._get_portions()
        return portions[index]
