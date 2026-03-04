from __future__ import annotations
from typing import TYPE_CHECKING, Any, List
from .ICommentAuthorCollection import ICommentAuthorCollection

if TYPE_CHECKING:
    from .CommentAuthor import CommentAuthor
    from .ICommentAuthor import ICommentAuthor
    from ._internal.pptx.comment_authors_part import CommentAuthorsPart


from ._internal.base_collection import BaseCollection
class CommentAuthorCollection(BaseCollection, ICommentAuthorCollection):
    """Represents a collection of comment authors."""

    def _init_internal(
        self,
        authors_part: 'CommentAuthorsPart',
        package,
        presentation=None,
    ) -> None:
        self._authors_part = authors_part
        self._package = package
        self._presentation = presentation

    def _build_author(self, data) -> 'CommentAuthor':
        from .CommentAuthor import CommentAuthor
        ca = CommentAuthor()
        ca._init_internal(data, self._authors_part, self._package, self._presentation)
        return ca

    @property
    def as_i_collection(self) -> list:
        return self.to_array()

    @property
    def as_i_enumerable(self) -> Any:
        return self.to_array()

    def add_author(self, name: str, initials: str) -> 'ICommentAuthor':
        """Add a new author at the end of the collection."""
        data = self._authors_part.add_author(name, initials)
        return self._build_author(data)

    def to_array(self) -> List['ICommentAuthor']:
        return [self._build_author(d) for d in self._authors_part.get_authors()]

    def find_by_name(self, name: str) -> List['ICommentAuthor']:
        return [
            self._build_author(d)
            for d in self._authors_part.get_authors()
            if d.name == name
        ]

    def find_by_name_and_initials(self, name: str, initials: str) -> List['ICommentAuthor']:
        return [
            self._build_author(d)
            for d in self._authors_part.get_authors()
            if d.name == name and d.initials == initials
        ]

    def remove_at(self, index: int) -> None:
        authors = self._authors_part.get_authors()
        if 0 <= index < len(authors):
            data = authors[index]
            self._build_author(data).comments.clear()
            self._authors_part.remove_author(data.id)

    def remove(self, author: 'ICommentAuthor') -> None:
        author.remove()

    def clear(self) -> None:
        for data in self._authors_part.get_authors():
            self._build_author(data).comments.clear()
        self._authors_part.clear()

    def __getitem__(self, index: int) -> 'CommentAuthor':
        authors = self._authors_part.get_authors()
        if index < 0 or index >= len(authors):
            raise IndexError(f"Index {index} out of range")
        return self._build_author(authors[index])

    def __len__(self) -> int:
        return len(self._authors_part.get_authors())
