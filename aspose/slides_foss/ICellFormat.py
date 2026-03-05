from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFillFormat import IFillFormat
    from .ILineFormat import ILineFormat

class ICellFormat(ABC):
    """Represents format of a table cell."""
    @property
    def fill_format(self) -> IFillFormat:
        """Returns a cell fill properties object. Read-only ."""
        ...

    @property
    def border_left(self) -> ILineFormat:
        """Returns a left border line properties object. Read-only ."""
        ...

    @property
    def border_top(self) -> ILineFormat:
        """Returns a top border line properties object. Read-only ."""
        ...

    @property
    def border_right(self) -> ILineFormat:
        """Returns a right border line properties object. Read-only ."""
        ...

    @property
    def border_bottom(self) -> ILineFormat:
        """Returns a bottom border line properties object. Read-only ."""
        ...

    @property
    def border_diagonal_down(self) -> ILineFormat:
        """Returns a top-left to bottom-right diagonal line properties object. Read-only ."""
        ...

    @property
    def border_diagonal_up(self) -> ILineFormat:
        """Returns a bottom-left to top-right diagonal line properties object. Read-only ."""
        ...




