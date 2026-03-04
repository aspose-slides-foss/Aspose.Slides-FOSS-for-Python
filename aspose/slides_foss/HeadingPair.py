from __future__ import annotations
from .IHeadingPair import IHeadingPair

class HeadingPair(IHeadingPair):
    """Represents a 'Heading pair' property of the document. It indicates the group name of document parts and the number of parts in group."""

    def _init_internal(self, name: str, count: int):
        self._name = name
        self._count = count

    @property
    def name(self) -> str:
        """Returns the group name of document parts. Read-only ."""
        if not hasattr(self, '_name'):
            return ''
        return self._name

    @property
    def count(self) -> int:
        """Returns the number of parts in group. Read-only ."""
        if not hasattr(self, '_count'):
            return 0
        return self._count
