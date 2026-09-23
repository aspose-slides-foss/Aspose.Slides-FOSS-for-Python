from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
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

    def _current_part(self) -> Optional['CommentsPart']:
        """This comment's part as the package holds it now, or None if it is gone.

        Every accessor reads its own copy of a comment part, and an edit writes
        its copy back whole, so a copy read before another edit was saved would
        undo that edit.  Edits therefore start from the package, not the copy.
        """
        from ._internal.pptx.comments_part import CommentsPart
        package = self._comments_part._package
        part_name = self._comments_part.part_name
        if not package.has_part(part_name):
            return None
        return CommentsPart(package, part_name)

    def _edit(self, change: Callable[['CommentData'], None]) -> None:
        """Apply ``change`` to this comment as the package holds it now, and save the part."""
        current = self._current_part()
        data = None
        if current is not None:
            data = current.find_comment_by_idx(self._data.author_id, self._data.idx)
        if current is None or data is None:
            # Removed since this handle was made: nothing in the file to change.
            change(self._data)
            return
        change(data)
        current.save()
        self._comments_part, self._data = current, data

    @property
    def text(self) -> str:
        """Returns or sets the plain text of a slide comment. Read/write str."""
        return self._data.text

    @text.setter
    def text(self, value: str):
        def change(data: 'CommentData') -> None:
            data.text = value
        self._edit(change)

    @property
    def created_time(self) -> Any:
        """Returns or sets the time of a comment creation. Read/write datetime."""
        from ._internal.pptx.comments_part import _str_to_dt
        return _str_to_dt(self._data.dt_str)

    @created_time.setter
    def created_time(self, value: Any):
        from ._internal.pptx.comments_part import _dt_to_str
        dt_str = _dt_to_str(value) if value is not None else ''

        def change(data: 'CommentData') -> None:
            data.dt_str = dt_str
        self._edit(change)

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
        """Returns or sets the position of a comment on a slide, in centimetres
        from the top-left corner of the slide. Read/write PointF."""
        from aspose.slides_foss.drawing import PointF
        return PointF(self._data.pos_x, self._data.pos_y)

    @position.setter
    def position(self, value: Any):
        def change(data: 'CommentData') -> None:
            data.pos_x = value.x
            data.pos_y = value.y
        self._edit(change)

    @property
    def parent_comment(self) -> Optional['IComment']:
        """Gets or sets parent comment. Read/write IComment."""
        parent_ref = self._data.parent_ref
        if parent_ref is None:
            return None
        cd = self._comments_part.find_comment_by_idx(parent_ref[0], parent_ref[1])
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
        parent_ref = None if value is None else (value._data.author_id, value._data.idx)

        def change(data: 'CommentData') -> None:
            data.parent_ref = parent_ref
        self._edit(change)

    def remove(self) -> None:
        """Removes comment and all its replies from the parent collection."""
        me = (self._data.author_id, self._data.idx)
        current = self._current_part()
        if current is None:
            return
        # This comment and every comment that replies to it, as the package holds them now.
        for cd in current.get_comments():
            if (cd.author_id, cd.idx) == me or cd.parent_ref == me:
                current.remove_comment_elem(cd._elem)
        current.save()
        self._comments_part = current
