"""
Base class for all collection types in aspose.slides_foss.

Provides common collection behaviour (length property, iteration, membership)
on top of the __len__ and __getitem__ that each concrete collection implements.
This class is internal and not part of the public API.
"""

from __future__ import annotations


class BaseCollection:
    """
    Internal base for every *Collection class.

    Concrete subclasses must implement:
      - __len__(self) -> int
      - __getitem__(self, index: int) -> item

    In return they automatically get:
      - .length property  (mirrors Aspose .NET ICollection.Count / len())
      - __iter__          (sequential index-based iteration)
      - __contains__      (identity + equality membership test)
    """

    @property
    def length(self) -> int:
        """Returns the number of elements. Read-only."""
        return len(self)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __contains__(self, item) -> bool:
        for x in self:
            if x is item or x == item:
                return True
        return False
