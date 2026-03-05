from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFillFormat import IFillFormat

class ITableFormat(ABC):
    """Represents format of a table."""
    @property
    def fill_format(self) -> IFillFormat:
        """Returns a table fill properties object. Read-only ."""
        ...




