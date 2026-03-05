from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .ICellCollection import ICellCollection
from .IBulkTextFormattable import IBulkTextFormattable

if TYPE_CHECKING:
    from .IColumnFormat import IColumnFormat

class IColumn(ICellCollection, IBulkTextFormattable, ABC):
    """Represents a column in a table."""
    @property
    def width(self) -> float:
        """Returns or sets the width of a column. Read/write ."""
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def column_format(self) -> IColumnFormat:
        """Returns the ColumnFormat object that contains formatting properties for this column. Read-only ."""
        ...

    @property
    def as_i_cell_collection(self) -> ICellCollection:
        """Allows to get base ICellCollection interface. Read-only ."""
        ...

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        """Allows to get base IBulkTextFormattable interface. Read-only ."""
        ...
