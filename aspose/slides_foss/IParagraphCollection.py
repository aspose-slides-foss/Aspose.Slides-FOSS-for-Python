from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IParagraph import IParagraph

class IParagraphCollection(ISlideComponent, IPresentationComponent, ABC):
    """Represents a collection of a paragraphs."""
    @property
    def count(self) -> int:
        """Gets the number of elements actually contained in the collection. Read-only ."""
        ...

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...

    @property
    def as_i_enumerable(self) -> Any:
        """Returns IEnumerable interface. Read-only ."""
        ...

    @overload
    def add(self, value) -> None:
        ...

    @overload
    def add(self, value) -> int:
        ...


    @overload
    def insert(self, index, value) -> None:
        ...

    @overload
    def insert(self, index, value) -> None:
        ...
    def clear(self) -> None:
        ...
    def remove_at(self, index) -> None:
        ...
    def remove(self, item) -> bool:
        ...
    def __getitem__(self, index: int) -> IParagraph:
        ...
