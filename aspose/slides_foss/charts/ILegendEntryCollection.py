from __future__ import annotations
from abc import ABC, abstractmethod

class ILegendEntryCollection(ABC):
    """Represents legends collection."""
    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        ...
