from __future__ import annotations
from typing import TYPE_CHECKING, Any
import copy
import lxml.etree as ET
from .IRowCollection import IRowCollection

if TYPE_CHECKING:
    from .IRow import IRow
    from .Row import Row

from ._internal.base_collection import BaseCollection
class RowCollection(BaseCollection, IRowCollection):
    """Represents table row collection."""

    def _init_internal(self, tbl_element, slide_part, parent_slide, table):
        from .Row import Row
        from ._internal.pptx.constants import Elements
        self._tbl_element = tbl_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._table = table

        self._rows = []
        row_idx = 0
        for tr in tbl_element.findall(Elements.A_TR):
            row = Row()
            row._init_internal(tr, row_idx, slide_part, parent_slide, table)
            self._rows.append(row)
            row_idx += 1
        return self

    def _rebuild(self):
        """Rebuild the rows list from the XML."""
        from .Row import Row
        from ._internal.pptx.constants import Elements
        self._rows = []
        row_idx = 0
        for tr in self._tbl_element.findall(Elements.A_TR):
            row = Row()
            row._init_internal(tr, row_idx, self._slide_part, self._parent_slide, self._table)
            self._rows.append(row)
            row_idx += 1

    @property
    def as_i_collection(self) -> list:
        return list(self._rows)

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._rows)

    def add_clone(self, templ, with_attached_rows) -> list[IRow]:
        new_tr = copy.deepcopy(templ._tr_element)
        self._tbl_element.append(new_tr)
        self._rebuild()
        if self._slide_part:
            self._slide_part.save()
        return [self._rows[-1]]

    def insert_clone(self, index, templ, with_attached_rows) -> list[IRow]:
        from ._internal.pptx.constants import Elements
        new_tr = copy.deepcopy(templ._tr_element)
        trs = self._tbl_element.findall(Elements.A_TR)
        if index < len(trs):
            trs[index].addprevious(new_tr)
        else:
            self._tbl_element.append(new_tr)
        self._rebuild()
        if self._slide_part:
            self._slide_part.save()
        return [self._rows[index]]

    def remove_at(self, first_row_index, with_attached_rows) -> None:
        from ._internal.pptx.constants import Elements
        trs = self._tbl_element.findall(Elements.A_TR)
        if first_row_index < 0 or first_row_index >= len(trs):
            raise IndexError(f"Row index {first_row_index} out of range")
        self._tbl_element.remove(trs[first_row_index])
        self._rebuild()
        if self._slide_part:
            self._slide_part.save()

    def __getitem__(self, index: int) -> Row:
        return self._rows[index]

    def __len__(self) -> int:
        if hasattr(self, '_rows'):
            return len(self._rows)
        return 0

    def __iter__(self):
        if hasattr(self, '_rows'):
            return iter(self._rows)
        return iter([])
