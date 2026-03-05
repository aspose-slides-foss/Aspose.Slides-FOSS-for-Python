from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any, Optional, List
from .ICommentCollection import ICommentCollection

if TYPE_CHECKING:
    from .Comment import Comment
    from .IComment import IComment
    from .ISlide import ISlide
    from ._internal.pptx.comments_part import CommentsPart
    from ._internal.pptx.comment_authors_part import CommentAuthorsPart, AuthorData


from ._internal.base_collection import BaseCollection
class CommentCollection(BaseCollection, ICommentCollection):
    """Represents a collection of comments of one author."""

    def _init_internal(
        self,
        author_data: 'AuthorData',
        authors_part: 'CommentAuthorsPart',
        package,
        presentation=None,
    ) -> None:
        self._author_data = author_data
        self._authors_part = authors_part
        self._package = package
        self._presentation = presentation

    def _resolve_slide(self, part_name: str):
        """Return the Slide object whose part name matches, or None."""
        if self._presentation is None:
            return None
        for slide in self._presentation.slides:
            if getattr(slide, '_part_name', None) == part_name:
                return slide
        return None

    def _get_author_obj(self) -> 'ICommentAuthor':
        """Resolve the owning CommentAuthor object."""
        # Circular avoidance: return a lazy proxy if needed; for now resolve directly
        from .CommentAuthor import CommentAuthor
        ca = CommentAuthor()
        ca._init_internal(self._author_data, self._authors_part, self._package)
        return ca

    def _get_all_comments_parts(self) -> List[tuple]:
        """
        Return list of (comments_part, slide) pairs across all slides
        that have comments by this author.
        """
        from ._internal.pptx.comments_part import CommentsPart
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.opc import RelationshipsManager

        result = []
        author_id = self._author_data.id

        # Enumerate all slide parts in the package
        for part_name in self._package.get_part_names():
            if not (part_name.startswith('ppt/slides/slide') and part_name.endswith('.xml')):
                continue
            cp = CommentsPart.load_for_slide(self._package, part_name)
            if cp is None:
                continue
            comments = cp.get_comments_by_author(author_id)
            if comments:
                result.append((cp, part_name))
        return result

    def _get_or_create_comments_part(self, slide_part_name: str, slide=None) -> 'CommentsPart':
        from ._internal.pptx.comments_part import CommentsPart
        # Use a cache on the authors_part to share CommentsPart instances
        cache = getattr(self._authors_part, '_cp_cache', None)
        if cache is None:
            self._authors_part._cp_cache = {}
            cache = self._authors_part._cp_cache
        if slide_part_name not in cache:
            cp = CommentsPart.load_for_slide(self._package, slide_part_name)
            if cp is None:
                cp = CommentsPart.create_for_slide(
                    self._package, slide_part_name,
                    slide_rels_manager=getattr(getattr(slide, '_slide_part', None), '_rels_manager', None)
                )
            cache[slide_part_name] = cp
        return cache[slide_part_name]

    def _build_comment(self, data, cp, slide_obj) -> 'Comment':
        from .Comment import Comment
        c = Comment()
        author_obj = self._get_author_obj()
        c._init_internal(
            data=data,
            comments_part=cp,
            authors_part=self._authors_part,
            slide=slide_obj,
            author=author_obj,
            package=self._package,
            presentation=self._presentation,
        )
        return c

    def _collect_my_comments(self) -> List[tuple]:
        """Return list of (CommentData, CommentsPart, slide_part_name)."""
        from ._internal.pptx.comments_part import CommentsPart
        author_id = self._author_data.id
        result = []
        for part_name in self._package.get_part_names():
            if not (part_name.startswith('ppt/slides/slide') and part_name.endswith('.xml')):
                continue
            cp = CommentsPart.load_for_slide(self._package, part_name)
            if cp is None:
                continue
            for cd in cp.get_comments_by_author(author_id):
                result.append((cd, cp, part_name))
        return result

    @property
    def as_i_collection(self) -> list:
        return self.to_array()

    @property
    def as_i_enumerable(self) -> Any:
        return self.to_array()



    def to_array(self, *args, **kwargs) -> list['IComment']:
        all_entries = self._collect_my_comments()
        comments = [self._build_comment(cd, cp, self._resolve_slide(pn)) for cd, cp, pn in all_entries]
        if args:
            start = args[0]
            count = args[1] if len(args) > 1 else len(comments) - start
            return comments[start:start + count]
        return comments

    def add_comment(self, text, slide, position, creation_time) -> 'IComment':
        """Add a comment to the end of this author's comment collection for the given slide."""
        from ._internal.pptx.comments_part import _dt_to_str
        author_id = self._author_data.id
        idx = self._authors_part.next_comment_idx(author_id)
        dt_str = _dt_to_str(creation_time)

        slide_part_name = slide._part_name
        cp = self._get_or_create_comments_part(slide_part_name, slide)
        data = cp.add_comment(
            author_id=author_id,
            idx=idx,
            text=text,
            pos_x=position.x,
            pos_y=position.y,
            dt_str=dt_str,
        )
        cp.save()  # persist to in-memory package so other accessors see the change
        self._authors_part.save()  # persist author lastIdx update
        return self._build_comment(data, cp, slide)


    def insert_comment(self, index, text, slide, position, creation_time) -> 'IComment':
        """Insert a comment at the given position in this author's comment list."""
        from ._internal.pptx.comments_part import _dt_to_str
        author_id = self._author_data.id
        idx = self._authors_part.next_comment_idx(author_id)
        dt_str = _dt_to_str(creation_time)

        slide_part_name = slide._part_name
        cp = self._get_or_create_comments_part(slide_part_name, slide)
        data = cp.insert_comment(
            index=index,
            author_id=author_id,
            idx=idx,
            text=text,
            pos_x=position.x,
            pos_y=position.y,
            dt_str=dt_str,
        )
        cp.save()
        self._authors_part.save()
        return self._build_comment(data, cp, slide)


    def remove_at(self, index: int) -> None:
        all_entries = self._collect_my_comments()
        if 0 <= index < len(all_entries):
            cd, cp, _ = all_entries[index]
            cp.remove_comment_elem(cd._elem)
            cp.save()

    def remove(self, comment) -> None:
        """Remove the given comment (and its replies) from the collection."""
        comment.remove()

    def clear(self) -> None:
        """Remove all comments by this author across all slides."""
        author_id = self._author_data.id
        from ._internal.pptx.comments_part import CommentsPart
        for part_name in self._package.get_part_names():
            if not (part_name.startswith('ppt/slides/slide') and part_name.endswith('.xml')):
                continue
            cp = CommentsPart.load_for_slide(self._package, part_name)
            if cp is None:
                continue
            for cd in cp.get_comments_by_author(author_id):
                cp.remove_comment_elem(cd._elem)
            cp.save()

    def find_comment_by_idx(self, idx) -> Optional['IComment']:
        """Find a comment by its idx value (unique per author)."""
        author_id = self._author_data.id
        from ._internal.pptx.comments_part import CommentsPart
        for part_name in self._package.get_part_names():
            if not (part_name.startswith('ppt/slides/slide') and part_name.endswith('.xml')):
                continue
            cp = CommentsPart.load_for_slide(self._package, part_name)
            if cp is None:
                continue
            cd = cp.find_comment_by_idx(author_id, idx)
            if cd is not None:
                return self._build_comment(cd, cp, self._resolve_slide(part_name))
        return None

    def __getitem__(self, index: int) -> 'Comment':
        all_entries = self._collect_my_comments()
        if index < 0 or index >= len(all_entries):
            raise IndexError(f"Index {index} out of range")
        cd, cp, pn = all_entries[index]
        return self._build_comment(cd, cp, self._resolve_slide(pn))

    def __len__(self) -> int:
        return len(self._collect_my_comments())
