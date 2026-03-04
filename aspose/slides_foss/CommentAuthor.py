from __future__ import annotations
from typing import TYPE_CHECKING
from .ICommentAuthor import ICommentAuthor

if TYPE_CHECKING:
    from .ICommentCollection import ICommentCollection
    from ._internal.pptx.comment_authors_part import CommentAuthorsPart, AuthorData


class CommentAuthor(ICommentAuthor):
    """Represents an author of comments."""

    def _init_internal(
        self,
        data: 'AuthorData',
        authors_part: 'CommentAuthorsPart',
        package,
        presentation=None,
    ) -> None:
        self._data = data
        self._authors_part = authors_part
        self._package = package
        self._presentation = presentation
        self._comments_cache = None

    @property
    def name(self) -> str:
        """Returns or sets the author's name. Read/write str."""
        return self._data.name

    @name.setter
    def name(self, value: str):
        self._data.name = value

    @property
    def initials(self) -> str:
        """Returns or sets the author's initials. Read/write str."""
        return self._data.initials

    @initials.setter
    def initials(self, value: str):
        self._data.initials = value

    @property
    def comments(self) -> 'ICommentCollection':
        """Returns the collection of comments made by this author. Read-only."""
        if self._comments_cache is None:
            from .CommentCollection import CommentCollection
            col = CommentCollection()
            col._init_internal(self._data, self._authors_part, self._package, self._presentation)
            self._comments_cache = col
        return self._comments_cache

    def remove(self) -> None:
        """Removes the author from the parent collection."""
        self.comments.clear()
        self._authors_part.remove_author(self._data.id)
