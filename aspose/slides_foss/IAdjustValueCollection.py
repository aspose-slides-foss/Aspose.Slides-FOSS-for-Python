from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IAdjustValue import IAdjustValue

class IAdjustValueCollection(ABC):
    """Reprasents a collection of shape's adjustments."""
    @property
    def as_i_collection(self) -> list:
        """Allows to get base ICollection interface. Read-only ."""
        ...

    @property
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interface. Read-only ."""
        ...
    def __getitem__(self, index: int) -> IAdjustValue:
        ...

