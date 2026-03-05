from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ICommentAuthor import ICommentAuthor
    from .ISlide import ISlide

class IComment(ABC):
    """Represents a comment on a slide."""
    @property
    def text(self) -> str:
        """Returns or sets the plain text of a slide comment. Read/write ."""
        ...

    @text.setter
    def text(self, value: str):
        ...

    @property
    def created_time(self) -> Any:
        """Returns or sets the time of a comment creation. Setting this property to means no comment time is set. Read/write ."""
        ...

    @created_time.setter
    def created_time(self, value: Any):
        ...

    @property
    def slide(self) -> ISlide:
        """Returns or sets the parent slide of a comment. Read-only ."""
        ...

    @property
    def author(self) -> ICommentAuthor:
        """Returns the author of a comment. Read-only ."""
        ...

    @property
    def position(self) -> Any:
        """Returns or sets the position of a comment on a slide. Read/write ."""
        ...

    @position.setter
    def position(self, value: Any):
        ...

    @property
    def parent_comment(self) -> IComment:
        """Gets or sets parent comment. Read/write ."""
        ...

    @parent_comment.setter
    def parent_comment(self, value: IComment):
        ...
    def remove(self) -> None:
        ...

