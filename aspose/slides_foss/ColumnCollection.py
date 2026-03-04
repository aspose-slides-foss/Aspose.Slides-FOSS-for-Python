from __future__ import annotations
from typing import TYPE_CHECKING, Any
import copy
import lxml.etree as ET
from .IColumnCollection import IColumnCollection

if TYPE_CHECKING:
    from .Column import Column
    from .IColumn import IColumn

from ._internal.base_collection import BaseCollection
class ColumnCollection(BaseCollection, IColumnCollection):
    """Represents collection of columns in a table."""

    def _init_internal(self, tbl_element, tbl_grid_element, slide_part, parent_slide, table):
        from .Column import Column
        from ._internal.pptx.constants import Elements
        self._tbl_element = tbl_element
        self._tbl_grid_element = tbl_grid_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._table = table

        self._columns = []
        col_idx = 0
        for grid_col in tbl_grid_element.findall(Elements.A_GRID_COL):
            col = Column()
            col._init_internal(grid_col, col_idx, tbl_element, slide_part, parent_slide, table)
            self._columns.append(col)
            col_idx += 1
        return self

    def _rebuild(self):
        """Rebuild column list from XML."""
        from .Column import Column
        from ._internal.pptx.constants import Elements
        self._columns = []
        col_idx = 0
        for grid_col in self._tbl_grid_element.findall(Elements.A_GRID_COL):
            col = Column()
            col._init_internal(grid_col, col_idx, self._tbl_element, self._slide_part, self._parent_slide, self._table)
            self._columns.append(col)
            col_idx += 1

    @property
    def as_i_collection(self) -> list:
        if hasattr(self, '_columns'):
            return list(self._columns)
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_enumerable(self) -> Any:
        if hasattr(self, '_columns'):
            return iter(self._columns)
        raise NotImplementedError("This feature is not yet available in this version.")

    def add_clone(self, templ, with_attached_columns) -> list[IColumn]:
        if not hasattr(self, '_tbl_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements

        # Clone the gridCol
        new_grid_col = copy.deepcopy(templ._grid_col_element)
        self._tbl_grid_element.append(new_grid_col)

        # Clone cells: for each row, clone the tc at the template column index
        src_col_idx = templ._col_index
        for tr in self._tbl_element.findall(Elements.A_TR):
            tcs = tr.findall(Elements.A_TC)
            if src_col_idx < len(tcs):
                new_tc = copy.deepcopy(tcs[src_col_idx])
            else:
                new_tc = self._make_empty_tc()
            tr.append(new_tc)

        self._rebuild()
        if self._slide_part:
            self._slide_part.save()
        return [self._columns[-1]]

    def insert_clone(self, index, templ, with_attached_columns) -> list[IColumn]:
        if not hasattr(self, '_tbl_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements

        # Clone and insert gridCol
        new_grid_col = copy.deepcopy(templ._grid_col_element)
        grid_cols = self._tbl_grid_element.findall(Elements.A_GRID_COL)
        if index < len(grid_cols):
            grid_cols[index].addprevious(new_grid_col)
        else:
            self._tbl_grid_element.append(new_grid_col)

        # Clone cells in each row
        src_col_idx = templ._col_index
        for tr in self._tbl_element.findall(Elements.A_TR):
            tcs = tr.findall(Elements.A_TC)
            if src_col_idx < len(tcs):
                new_tc = copy.deepcopy(tcs[src_col_idx])
            else:
                new_tc = self._make_empty_tc()
            if index < len(tcs):
                tcs[index].addprevious(new_tc)
            else:
                tr.append(new_tc)

        self._rebuild()
        if self._slide_part:
            self._slide_part.save()
        return [self._columns[index]]

    def remove_at(self, first_column_index, with_attached_rows) -> None:
        if not hasattr(self, '_tbl_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements

        # Remove gridCol
        grid_cols = self._tbl_grid_element.findall(Elements.A_GRID_COL)
        if first_column_index < 0 or first_column_index >= len(grid_cols):
            raise IndexError(f"Column index {first_column_index} out of range")
        self._tbl_grid_element.remove(grid_cols[first_column_index])

        # Remove corresponding tc from each row
        for tr in self._tbl_element.findall(Elements.A_TR):
            tcs = tr.findall(Elements.A_TC)
            if first_column_index < len(tcs):
                tr.remove(tcs[first_column_index])

        self._rebuild()
        if self._slide_part:
            self._slide_part.save()

    @staticmethod
    def _make_empty_tc():
        """Create an empty <a:tc> element with txBody and tcPr."""
        from ._internal.pptx.constants import Elements, NS
        tc = ET.Element(Elements.A_TC)
        txbody = ET.SubElement(tc, Elements.A_TX_BODY)
        ET.SubElement(txbody, Elements.A_BODY_PR)
        ET.SubElement(txbody, Elements.A_LST_STYLE)
        p = ET.SubElement(txbody, Elements.A_P)
        ET.SubElement(p, Elements.A_END_PARA_RPR)
        ET.SubElement(tc, Elements.A_TC_PR)
        return tc

    def __getitem__(self, index: int) -> Column:
        if hasattr(self, '_columns'):
            return self._columns[index]
        raise NotImplementedError("This feature is not yet available in this version.")

    def __len__(self) -> int:
        if hasattr(self, '_columns'):
            return len(self._columns)
        return 0

    def __iter__(self):
        if hasattr(self, '_columns'):
            return iter(self._columns)
        return iter([])
