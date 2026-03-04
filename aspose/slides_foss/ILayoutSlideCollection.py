from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide

class ILayoutSlideCollection(ABC):
    """Represents a base class for collection of a layout slides."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...
    def get_by_type(self, type) -> ILayoutSlide:
        ...
    def __getitem__(self, index: int) -> ILayoutSlide:
        ...

