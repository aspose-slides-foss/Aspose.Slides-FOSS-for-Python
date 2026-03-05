from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class INotesSize(ABC):
    """Represents a size of notes slide."""
    @property
    def size(self) -> Any:
        """Returns or sets the size in points. Read/write ."""
        ...

    @size.setter
    def size(self, value: Any):
        ...

