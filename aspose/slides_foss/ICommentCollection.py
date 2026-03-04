from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IComment import IComment
    from .IModernComment import IModernComment

class ICommentCollection(ABC):
    """Represents a collection of comments of one author."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...

    @overload
    def to_array(self) -> list[IComment]:
        ...

    @overload
    def to_array(self, start_index, count) -> list[IComment]:
        ...
    def add_comment(self, text, slide, position, creation_time) -> IComment:
        ...
    def insert_comment(self, index, text, slide, position, creation_time) -> IComment:
        ...
    def remove_at(self, index) -> None:
        ...
    def remove(self, comment) -> None:
        ...
    def clear(self) -> None:
        ...
    def __getitem__(self, index: int) -> IComment:
        ...

