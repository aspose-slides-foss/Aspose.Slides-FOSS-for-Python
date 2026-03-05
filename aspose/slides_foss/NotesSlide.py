from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING
from .BaseSlide import BaseSlide
from .INotesSlide import INotesSlide

if TYPE_CHECKING:
    from .INotesSlideHeaderFooterManager import INotesSlideHeaderFooterManager
    from .ISlide import ISlide
    from .ITextFrame import ITextFrame
    from .IBaseSlide import IBaseSlide
    from ._internal.pptx.notes_slide_part import NotesSlidePart
    from ._internal.opc import OpcPackage


class NotesSlide(BaseSlide, INotesSlide):
    """Represents a notes slide in a presentation."""

    def _init_internal(
        self,
        presentation,
        package: OpcPackage,
        part_name: str,
        notes_part: NotesSlidePart,
        parent_slide: ISlide,
    ) -> None:
        """
        Internal initialization for a notes slide.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            part_name: The part name of this notes slide.
            notes_part: The parsed NotesSlidePart.
            parent_slide: The Slide that owns this notes slide.
        """
        super().__init__()
        self._presentation_ref = presentation
        self._package = package
        self._part_name = part_name
        self._notes_part = notes_part
        self._parent_slide = parent_slide
        self._header_footer_manager_cache: Optional[INotesSlideHeaderFooterManager] = None

    def _get_slide_part(self):
        """Return the notes slide part for BaseSlide shape access."""
        if hasattr(self, '_notes_part'):
            return self._notes_part
        return None

    @property
    def header_footer_manager(self) -> INotesSlideHeaderFooterManager:
        """Returns HeaderFooter manager of the notes slide. Read-only."""
        if self._header_footer_manager_cache is None:
            from .NotesSlideHeaderFooterManager import NotesSlideHeaderFooterManager
            mgr = NotesSlideHeaderFooterManager()
            mgr._init_internal(self._notes_part)
            self._header_footer_manager_cache = mgr
        return self._header_footer_manager_cache

    @property
    def notes_text_frame(self) -> Optional[ITextFrame]:
        """Returns a TextFrame with notes' text if there is one. Read-only."""
        if self._notes_part is None:
            return None
        txbody = self._notes_part.get_notes_txbody()
        if txbody is None:
            return None
        from .TextFrame import TextFrame
        tf = TextFrame()
        tf._init_internal(txbody, self._notes_part, self)
        return tf


    @property
    def parent_slide(self) -> ISlide:
        """Returns the parent slide. Read-only."""
        return self._parent_slide

    @property
    def as_i_base_slide(self) -> IBaseSlide:
        return self

