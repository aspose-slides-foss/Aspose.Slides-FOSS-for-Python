from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IColumn import IColumn

class IColumnCollection(ABC):
    """Represents collection of columns in a table."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...
    def add_clone(self, templ, with_attached_columns) -> list[IColumn]:
        ...
    def insert_clone(self, index, templ, with_attached_columns) -> list[IColumn]:
        ...
    def remove_at(self, first_column_index, with_attached_rows) -> None:
        ...
    def __getitem__(self, index: int) -> IColumn:
        ...

