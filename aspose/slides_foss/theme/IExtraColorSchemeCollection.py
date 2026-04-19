from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IExtraColorScheme import IExtraColorScheme

class IExtraColorSchemeCollection(ABC):
    """Represents a collection of additional color schemes."""
    @property
    @abstractmethod
    def as_i_collection(self) -> list:
        ...

    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> IExtraColorScheme:
        ...

