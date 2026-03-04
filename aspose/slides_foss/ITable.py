from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IGraphicalObject import IGraphicalObject
from .IBulkTextFormattable import IBulkTextFormattable

if TYPE_CHECKING:
    from .ICell import ICell
    from .IColumnCollection import IColumnCollection
    from .IRowCollection import IRowCollection
    from .ITableFormat import ITableFormat
    from .TableStylePreset import TableStylePreset

class ITable(IGraphicalObject, IBulkTextFormattable, ABC):
    """Represents a table on a slide."""
    @property
    def rows(self) -> IRowCollection:
        """Returns the collectoin of rows. Read-only ."""
        ...

    @property
    def columns(self) -> IColumnCollection:
        """Returns the collectoin of columns. Read-only ."""
        ...

    @property
    def table_format(self) -> ITableFormat:
        """Returns the TableFormat object that contains formatting properties for this table. Read-only ."""
        ...

    @property
    def style_preset(self) -> TableStylePreset:
        """Get's or sets builtin table style. Read/write ."""
        ...

    @style_preset.setter
    def style_preset(self, value: TableStylePreset):
        ...

    @property
    def right_to_left(self) -> bool:
        """Determines whether the table has right to left reading order. Read-write ."""
        ...

    @right_to_left.setter
    def right_to_left(self, value: bool):
        ...

    @property
    def first_row(self) -> bool:
        """Determines whether the first row of a table has to be drawn with a special formatting. Read/write ."""
        ...

    @first_row.setter
    def first_row(self, value: bool):
        ...

    @property
    def first_col(self) -> bool:
        """Determines whether the first column of a table has to be drawn with a special formatting. Read/write ."""
        ...

    @first_col.setter
    def first_col(self, value: bool):
        ...

    @property
    def last_row(self) -> bool:
        """Determines whether the last row of a table has to be drawn with a special formatting. Read/write ."""
        ...

    @last_row.setter
    def last_row(self, value: bool):
        ...

    @property
    def last_col(self) -> bool:
        """Determines whether the last column of a table has to be drawn with a special formatting. Read/write ."""
        ...

    @last_col.setter
    def last_col(self, value: bool):
        ...

    @property
    def horizontal_banding(self) -> bool:
        """Determines whether the even rows has to be drawn with a different formatting. Read/write ."""
        ...

    @horizontal_banding.setter
    def horizontal_banding(self, value: bool):
        ...

    @property
    def vertical_banding(self) -> bool:
        """Determines whether the even columns has to be drawn with a different formatting. Read/write ."""
        ...

    @vertical_banding.setter
    def vertical_banding(self, value: bool):
        ...

    @property
    def as_i_graphical_object(self) -> IGraphicalObject:
        """Allows to get base IGraphicalObject interface. Read-only ."""
        ...

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        """Allows to get base IBulkTextFormattable interface. Read-only ."""
        ...
    def merge_cells(self, cell1, cell2, allow_splitting) -> ICell:
        ...
