from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .CellCollection import CellCollection
from .IColumn import IColumn

if TYPE_CHECKING:
    from .IBulkTextFormattable import IBulkTextFormattable
    from .ICellCollection import ICellCollection

class Column(CellCollection, IColumn):
    """Represents a column in a table."""

    def _init_internal(self, grid_col_element, col_index, tbl_element, slide_part, parent_slide, table):
        from .Cell import Cell
        from ._internal.pptx.constants import Elements
        self._grid_col_element = grid_col_element
        self._col_index = col_index
        self._tbl_element = tbl_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._table_ref = table

        # Parse cells: one per row at this column index
        cells = []
        row_idx = 0
        for tr in tbl_element.findall(Elements.A_TR):
            tcs = tr.findall(Elements.A_TC)
            if col_index < len(tcs):
                cell = Cell()
                cell._init_internal(tcs[col_index], row_idx, col_index, slide_part, parent_slide, table)
                cells.append(cell)
            row_idx += 1
        self._cells = cells
        return self

    @property
    def width(self) -> float:
        """Returns or sets the width of a column. Read/write ."""
        if hasattr(self, '_grid_col_element') and self._grid_col_element is not None:
            from ._internal.pptx.constants import EMU_PER_POINT
            w = self._grid_col_element.get('w')
            if w is not None:
                return int(w) / EMU_PER_POINT
        return 0.0

    @width.setter
    def width(self, value: float):
        if hasattr(self, '_grid_col_element') and self._grid_col_element is not None:
            from ._internal.pptx.constants import EMU_PER_POINT
            self._grid_col_element.set('w', str(int(round(value * EMU_PER_POINT))))
            if self._slide_part:
                self._slide_part.save()

    @property
    def column_format(self) -> IColumnFormat:
        """Returns the ColumnFormat object that contains formatting properties for this column. Read-only ."""
        from .ColumnFormat import ColumnFormat
        return ColumnFormat()

    @property
    def as_i_cell_collection(self) -> ICellCollection:
        return self

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        return self




    def set_text_format(self, *args, **kwargs) -> None:
        if len(args) < 1:
            raise ValueError("set_text_format requires at least 1 argument")
        source = args[0]
        from ._internal.pptx.bulk_text_format import apply_text_format
        apply_text_format(list(self), source, self._slide_part)
