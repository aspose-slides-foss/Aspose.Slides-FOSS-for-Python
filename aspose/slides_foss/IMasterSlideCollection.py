from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IMasterSlide import IMasterSlide

class IMasterSlideCollection(ABC):
    """Represents a collection of master slides."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...
    def add_clone(self, source_master) -> IMasterSlide:
        ...
    def __getitem__(self, index: int) -> IMasterSlide:
        ...

