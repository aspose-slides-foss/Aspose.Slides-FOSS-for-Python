from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IEffectStyle import IEffectStyle

class IEffectStyleCollection(ABC):
    """Represents a collection of effect styles."""
    @property
    @abstractmethod
    def as_i_collection(self) -> list:
        ...

    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> IEffectStyle:
        ...

