from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ICommentCollection import ICommentCollection

class ICommentAuthor(ABC):
    """Represents an author of comments."""
    @property
    def name(self) -> str:
        """Returns or sets the author's name. Read/write ."""
        ...

    @name.setter
    def name(self, value: str):
        ...

    @property
    def initials(self) -> str:
        """Returns or sets the authors initials. Read/write ."""
        ...

    @initials.setter
    def initials(self, value: str):
        ...

    @property
    def comments(self) -> ICommentCollection:
        """Returns the collection of comments made by this author. Read-only ."""
        ...
    def remove(self) -> None:
        ...

