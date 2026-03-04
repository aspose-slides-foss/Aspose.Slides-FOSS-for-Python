from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .ICellCollection import ICellCollection
from .IBulkTextFormattable import IBulkTextFormattable

if TYPE_CHECKING:
    from .IRowFormat import IRowFormat

class IRow(ICellCollection, IBulkTextFormattable, ABC):
    """Represents a row in a table."""
    @property
    def height(self) -> float:
        """Returns the height of a row. Read-only ."""
        ...

    @property
    def minimal_height(self) -> float:
        """Returns or sets the minimal possible height of a row. Read/write ."""
        ...

    @minimal_height.setter
    def minimal_height(self, value: float):
        ...

    @property
    def row_format(self) -> IRowFormat:
        """Returns the RowFormat object that contains formatting properties for this row. Read-only ."""
        ...

    @property
    def as_i_cell_collection(self) -> ICellCollection:
        """Allows to get base ICellCollection interface. Read-only ."""
        ...

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        """Allows to get base IBulkTextFormattable interface. Read-only ."""
        ...
