from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..IFillFormat import IFillFormat

class IFillFormatCollection(ABC):
    """Represents the collection of fill styles."""
    @property
    @abstractmethod
    def as_i_collection(self) -> list:
        ...

    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> IFillFormat:
        ...

