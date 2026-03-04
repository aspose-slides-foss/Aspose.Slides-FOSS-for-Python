from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .CellCollection import CellCollection
from .IRow import IRow

if TYPE_CHECKING:
    from .IBulkTextFormattable import IBulkTextFormattable
    from .ICellCollection import ICellCollection
    from .IRowFormat import IRowFormat

class Row(CellCollection, IRow):
    """Represents a row in a table."""

    def _init_internal(self, tr_element, row_index, slide_part, parent_slide, table):
        from .Cell import Cell
        from ._internal.pptx.constants import Elements
        self._tr_element = tr_element
        self._row_index = row_index
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._table_ref = table

        # Parse cells from <a:tc> children
        cells = []
        col_idx = 0
        for tc in tr_element.findall(Elements.A_TC):
            cell = Cell()
            cell._init_internal(tc, row_index, col_idx, slide_part, parent_slide, table)
            cells.append(cell)
            col_idx += 1
        self._cells = cells
        return self

    @property
    def height(self) -> float:
        """Returns the height of a row. Read-only ."""
        if hasattr(self, '_tr_element') and self._tr_element is not None:
            from ._internal.pptx.constants import EMU_PER_POINT
            h = self._tr_element.get('h')
            if h is not None:
                return int(h) / EMU_PER_POINT
        return 0.0

    @property
    def minimal_height(self) -> float:
        """Returns or sets the minimal possible height of a row. Read/write ."""
        if hasattr(self, '_tr_element') and self._tr_element is not None:
            from ._internal.pptx.constants import EMU_PER_POINT
            h = self._tr_element.get('h')
            if h is not None:
                return int(h) / EMU_PER_POINT
        return 0.0

    @minimal_height.setter
    def minimal_height(self, value: float):
        if hasattr(self, '_tr_element') and self._tr_element is not None:
            from ._internal.pptx.constants import EMU_PER_POINT
            self._tr_element.set('h', str(int(round(value * EMU_PER_POINT))))
            if self._slide_part:
                self._slide_part.save()

    @property
    def row_format(self) -> IRowFormat:
        """Returns the RowFormat object that contains formatting properties for this row. Read-only ."""
        from .RowFormat import RowFormat
        return RowFormat()

    @property
    def as_i_cell_collection(self) -> ICellCollection:
        return self

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        return self




    def set_text_format(self, *args, **kwargs) -> None:
        if len(args) < 1:
            raise NotImplementedError("This feature is not yet available in this version.")
        source = args[0]
        from ._internal.pptx.bulk_text_format import apply_text_format
        apply_text_format(list(self), source, self._slide_part)
