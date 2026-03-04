from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .INotesSlideManager import INotesSlideManager

if TYPE_CHECKING:
    from .INotesSlide import INotesSlide
    from .ISlide import ISlide
    from ._internal.opc import OpcPackage
    from ._internal.pptx.slide_part import SlidePart


class NotesSlideManager(INotesSlideManager):
    """Notes slide manager."""

    def _init_internal(
        self,
        slide: ISlide,
        package: OpcPackage,
        slide_part: SlidePart,
    ) -> None:
        """
        Internal initialization.

        Args:
            slide: The parent Slide object.
            package: The OPC package.
            slide_part: The SlidePart for managing relationships.
        """
        self._slide = slide
        self._package = package
        self._slide_part = slide_part
        self._notes_slide_cache: Optional[INotesSlide] = None

    def _get_notes_part_name(self) -> Optional[str]:
        """
        Resolve the notes slide part name from the slide's relationships.

        Returns:
            The part name string, or None if no notes slide relationship exists.
        """
        from ._internal.opc.relationships import REL_TYPES
        rels = self._slide_part._rels_manager.get_relationships_by_type(
            REL_TYPES['notes_slide']
        )
        if rels:
            return self._slide_part._resolve_target(rels[0].target)
        return None

    @property
    def notes_slide(self) -> Optional[INotesSlide]:
        """Returns the notes slide for the current slide. Returns null if slide doesn't have notes slide. Read-only."""
        if self._notes_slide_cache is not None:
            return self._notes_slide_cache

        part_name = self._get_notes_part_name()
        if part_name is None:
            return None

        return self._load_notes_slide(part_name)

    def _load_notes_slide(self, part_name: str) -> INotesSlide:
        """Load and cache a NotesSlide from the given part name."""
        from ._internal.pptx.notes_slide_part import NotesSlidePart
        from .NotesSlide import NotesSlide

        notes_part = NotesSlidePart(self._package, part_name)
        notes_slide = NotesSlide()
        notes_slide._init_internal(
            presentation=self._slide._presentation_ref
            if hasattr(self._slide, '_presentation_ref') else None,
            package=self._package,
            part_name=part_name,
            notes_part=notes_part,
            parent_slide=self._slide,
        )
        self._notes_slide_cache = notes_slide
        return notes_slide

    def add_notes_slide(self) -> INotesSlide:
        """Returns the notes slide for the current slide, creating one if it doesn't exist."""
        existing = self.notes_slide
        if existing is not None:
            return existing

        from ._internal.pptx.notes_slide_part import NotesSlidePart
        from ._internal.opc.relationships import REL_TYPES

        slide_part_name = self._slide_part.part_name

        # Create the notes slide XML part
        notes_part = NotesSlidePart.create_empty(self._package, slide_part_name)
        notes_part_name = notes_part.part_name

        # Add relationship from slide → notes slide
        relative_target = NotesSlidePart._compute_relative_target(
            slide_part_name, notes_part_name
        )
        self._slide_part._rels_manager.add_relationship(
            REL_TYPES['notes_slide'], relative_target
        )
        self._slide_part._rels_manager.save()

        return self._load_notes_slide(notes_part_name)

    def remove_notes_slide(self) -> None:
        """Removes the notes slide of the current slide."""
        from ._internal.opc.relationships import REL_TYPES
        from ._internal.pptx.notes_slide_part import NotesSlidePart

        part_name = self._get_notes_part_name()
        if part_name is None:
            return

        # Remove relationship from slide → notes slide
        rels = self._slide_part._rels_manager.get_relationships_by_type(
            REL_TYPES['notes_slide']
        )
        for rel in rels:
            self._slide_part._rels_manager.remove_relationship(rel.id)
        self._slide_part._rels_manager.save()

        # Delete the notes slide part files
        NotesSlidePart.delete(self._package, part_name)

        # Clear cache
        self._notes_slide_cache = None
