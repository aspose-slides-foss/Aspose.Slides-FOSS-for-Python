from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ISlide import ISlide

class ISlideCollection(ABC):
    """Represents a collection of a slides."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...

    @overload
    def add_clone(self, source_slide) -> ISlide:
        ...

    @overload
    def add_clone(self, source_slide, section) -> ISlide:
        ...

    @overload
    def add_clone(self, source_slide, dest_layout) -> ISlide:
        ...

    @overload
    def add_clone(self, source_slide, dest_master, allow_clone_missing_layout) -> ISlide:
        ...


    @overload
    def insert_clone(self, index, source_slide) -> ISlide:
        ...

    @overload
    def insert_clone(self, index, source_slide, dest_layout) -> ISlide:
        ...

    @overload
    def insert_clone(self, index, source_slide, dest_master, allow_clone_missing_layout) -> ISlide:
        ...


    @overload
    def to_array(self) -> list[ISlide]:
        ...

    @overload
    def to_array(self, start_index, count) -> list[ISlide]:
        ...
    def add_empty_slide(self, layout) -> ISlide:
        ...
    def insert_empty_slide(self, index, layout) -> ISlide:
        ...
    def remove(self, value) -> None:
        ...
    def remove_at(self, index) -> None:
        ...
    def index_of(self, slide) -> int:
        ...
    def __getitem__(self, index: int) -> ISlide:
        ...

