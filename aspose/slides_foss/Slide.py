from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING
from .BaseSlide import BaseSlide
from .ISlide import ISlide

if TYPE_CHECKING:
    from .IComment import IComment
    from .IImage import IImage
    from .ILayoutSlide import ILayoutSlide
    from .INotesSlideManager import INotesSlideManager
    from .theme.IOverrideThemeManager import IOverrideThemeManager
    from ._internal.pptx.slide_part import SlidePart
    from ._internal.pptx.presentation_part import SlideReference
    from ._internal.opc import OpcPackage

class Slide(BaseSlide, ISlide):
    """Represents a slide in a presentation."""

    def _init_internal(self, presentation, package: OpcPackage,
                       part_name: str, slide_ref: SlideReference,
                       slide_part: SlidePart,
                       layout_resolver=None) -> None:
        """
        Internal initialization for a slide.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            part_name: The part name of this slide.
            slide_ref: The SlideReference from PresentationPart.
            slide_part: The parsed SlidePart.
            layout_resolver: Callable(part_name) -> LayoutSlide.
        """
        super().__init__()
        self._presentation_ref = presentation
        self._package = package
        self._part_name = part_name
        self._slide_ref = slide_ref
        self._slide_part = slide_part
        self._layout_resolver = layout_resolver
        self._layout_slide_cache: Optional[ILayoutSlide] = None
        self._notes_slide_manager_cache: Optional[INotesSlideManager] = None



    @property
    def slide_number(self) -> int:
        """Returns a number of slide. Index of slide in collection is always equal to SlideNumber - Presentation.FirstSlideNumber. Read/write ."""
        if hasattr(self, '_presentation_ref') and self._presentation_ref is not None:
            slides = self._presentation_ref.slides
            for i in range(len(slides)):
                if slides[i].slide_id == self.slide_id:
                    return i + self._presentation_ref.first_slide_number
        return 0


    @property
    def hidden(self) -> bool:
        """Determines whether the specified slide is hidden during a slide show. Read/write ."""
        if hasattr(self, '_slide_part') and self._slide_part is not None:
            return self._slide_part.hidden
        return False

    @hidden.setter
    def hidden(self, value: bool):
        if hasattr(self, '_slide_part') and self._slide_part is not None:
            self._slide_part.hidden = value

    @property
    def layout_slide(self) -> ILayoutSlide:
        """Returns or sets the layout slide for the current slide. Read/write ."""
        if hasattr(self, '_layout_resolver') and self._layout_resolver is not None:
            if self._layout_slide_cache is None:
                layout_part_name = self._slide_part.layout_part_name
                if layout_part_name:
                    self._layout_slide_cache = self._layout_resolver(layout_part_name)
            if self._layout_slide_cache is not None:
                return self._layout_slide_cache
        return None


    @property
    def theme_manager(self) -> IOverrideThemeManager:
        """Returns the overriding theme manager. Read-only ."""
        if not hasattr(self, '_theme_manager_cache') or self._theme_manager_cache is None:
            from .theme.SlideThemeManager import SlideThemeManager
            mgr = SlideThemeManager()
            mgr._init_internal()
            self._theme_manager_cache = mgr
        return self._theme_manager_cache

    @property
    def notes_slide_manager(self) -> INotesSlideManager:
        """Allow to access notes slide, add and remove it. Read-only."""
        if self._notes_slide_manager_cache is None:
            from .NotesSlideManager import NotesSlideManager
            mgr = NotesSlideManager()
            mgr._init_internal(
                slide=self,
                package=self._package,
                slide_part=self._slide_part,
            )
            self._notes_slide_manager_cache = mgr
        return self._notes_slide_manager_cache















    def remove(self) -> None:
        if hasattr(self, '_presentation_ref') and self._presentation_ref is not None:
            self._presentation_ref.slides.remove(self)


    def get_slide_comments(self, author) -> 'ICommentList':
        """
        Returns all comments on this slide, optionally filtered by author.
        Pass None to get comments from all authors.
        """
        class ICommentList(list):
            """list subclass that also exposes .length for .NET API compatibility."""
            @property
            def length(self):
                return len(self)

        from ._internal.pptx.comments_part import CommentsPart
        cp = CommentsPart.load_for_slide(self._package, self._part_name)
        if cp is None:
            return ICommentList()

        if author is None:
            from .Comment import Comment as CommentImpl
            from .CommentAuthor import CommentAuthor as CommentAuthorImpl
            from ._internal.pptx.comment_authors_part import CommentAuthorsPart
            authors_part = CommentAuthorsPart(self._package)
            result = ICommentList()
            for cd in cp.get_comments():
                author_data = authors_part.find_author_by_id(cd.author_id)
                if author_data is None:
                    continue
                ca = CommentAuthorImpl()
                ca._init_internal(author_data, authors_part, self._package, self._presentation_ref)
                c = CommentImpl()
                c._init_internal(
                    data=cd,
                    comments_part=cp,
                    authors_part=authors_part,
                    slide=self,
                    author=ca,
                    package=self._package,
                    presentation=self._presentation_ref,
                )
                result.append(c)
            return result
        else:
            author_id = author._data.id
            from .Comment import Comment as CommentImpl
            result = ICommentList()
            for cd in cp.get_comments_by_author(author_id):
                c = CommentImpl()
                c._init_internal(
                    data=cd,
                    comments_part=cp,
                    authors_part=author._authors_part,
                    slide=self,
                    author=author,
                    package=self._package,
                    presentation=self._presentation_ref,
                )
                result.append(c)
            return result

