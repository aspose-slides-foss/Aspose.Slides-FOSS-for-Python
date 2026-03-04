from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
from .IComment import IComment

if TYPE_CHECKING:
    from .ICommentAuthor import ICommentAuthor
    from .ISlide import ISlide
    from ._internal.pptx.comments_part import CommentData, CommentsPart
    from ._internal.pptx.comment_authors_part import CommentAuthorsPart


class Comment(IComment):
    """Represents a comment on a slide."""

    def _init_internal(
        self,
        data: 'CommentData',
        comments_part: 'CommentsPart',
        authors_part: 'CommentAuthorsPart',
        slide: 'ISlide',
        author: 'ICommentAuthor',
        package=None,
        presentation=None,
    ) -> None:
        self._data = data
        self._comments_part = comments_part
        self._authors_part = authors_part
        self._slide_ref = slide
        self._author_ref = author
        self._package = package
        self._presentation = presentation

    @property
    def text(self) -> str:
        """Returns or sets the plain text of a slide comment. Read/write str."""
        return self._data.text

    @text.setter
    def text(self, value: str):
        self._data.text = value

    @property
    def created_time(self) -> Any:
        """Returns or sets the time of a comment creation. Read/write datetime."""
        from ._internal.pptx.comments_part import _str_to_dt
        return _str_to_dt(self._data.dt_str)

    @created_time.setter
    def created_time(self, value: Any):
        from ._internal.pptx.comments_part import _dt_to_str
        self._data.dt_str = _dt_to_str(value) if value is not None else ''

    @property
    def slide(self) -> 'ISlide':
        """Returns the parent slide of a comment. Read-only."""
        return self._slide_ref

    @property
    def author(self) -> 'ICommentAuthor':
        """Returns the author of a comment. Read-only."""
        return self._author_ref

    @property
    def position(self) -> Any:
        """Returns or sets the position of a comment on a slide. Read/write PointF."""
        from aspose.slides_foss.drawing import PointF
        return PointF(self._data.pos_x, self._data.pos_y)

    @position.setter
    def position(self, value: Any):
        self._data.pos_x = value.x
        self._data.pos_y = value.y

    @property
    def parent_comment(self) -> Optional['IComment']:
        """Gets or sets parent comment. Read/write IComment."""
        parent_id = self._data.parent_cm_id
        if parent_id is None:
            return None
        # parentCmId references idx globally across all authors in the slide
        cd = self._comments_part.find_comment_by_idx_all(parent_id)
        if cd is None:
            return None
        author_data = self._authors_part.find_author_by_id(cd.author_id)
        if author_data is None:
            return None
        from .CommentAuthor import CommentAuthor
        author = CommentAuthor()
        author._init_internal(author_data, self._authors_part, self._package, self._presentation)
        parent = Comment()
        parent._init_internal(
            data=cd,
            comments_part=self._comments_part,
            authors_part=self._authors_part,
            slide=self._slide_ref,
            author=author,
            package=self._package,
            presentation=self._presentation,
        )
        return parent

    @parent_comment.setter
    def parent_comment(self, value: Optional['IComment']):
        if value is None:
            self._data.parent_cm_id = None
        else:
            self._data.parent_cm_id = value._data.idx

    def remove(self) -> None:
        """Removes comment and all its replies from the parent collection."""
        my_idx = self._data.idx
        my_author_id = self._data.author_id
        # Remove all replies that have this comment as their parent
        to_remove = []
        for cd in self._comments_part.get_comments_by_author(my_author_id):
            if cd.parent_cm_id == my_idx:
                to_remove.append(cd._elem)
        for elem in to_remove:
            self._comments_part.remove_comment_elem(elem)
        # Remove this comment itself
        self._comments_part.remove_comment_elem(self._data._elem)
        # Persist to package so subsequent loads see the change
        self._comments_part.save()
