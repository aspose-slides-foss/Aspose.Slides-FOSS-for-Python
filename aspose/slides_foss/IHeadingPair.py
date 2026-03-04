from __future__ import annotations
from abc import ABC, abstractmethod

class IHeadingPair(ABC):
    """Represents a 'Heading pair' property of the document. It indicates the group name of document parts and the number of parts in group."""
    @property
    def name(self) -> str:
        """Returns the group name of document parts. Read-only ."""
        ...

    @property
    def count(self) -> int:
        """Returns the number of parts in group. Read-only ."""
        ...

