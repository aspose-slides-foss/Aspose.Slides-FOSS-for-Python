from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IRow import IRow

class IRowCollection(ABC):
    """Represents table row collection."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...
    def add_clone(self, templ, with_attached_rows) -> list[IRow]:
        ...
    def insert_clone(self, index, templ, with_attached_rows) -> list[IRow]:
        ...
    def remove_at(self, first_row_index, with_attached_rows) -> None:
        ...
    def __getitem__(self, index: int) -> IRow:
        ...

