from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseHandoutNotesSlideHeaderFooterManager import BaseHandoutNotesSlideHeaderFooterManager
from .INotesSlideHeaderFooterManager import INotesSlideHeaderFooterManager

if TYPE_CHECKING:
    from ._internal.pptx.notes_slide_part import NotesSlidePart


class NotesSlideHeaderFooterManager(BaseHandoutNotesSlideHeaderFooterManager, INotesSlideHeaderFooterManager):
    """Represents manager which holds behavior of the notes slide placeholders, including header placeholder."""

    def _init_internal(self, notes_part: NotesSlidePart) -> None:
        """
        Internal initialization.

        Args:
            notes_part: The NotesSlidePart providing placeholder access.
        """
        self._notes_part = notes_part

    # --- Visibility properties ---

    @property
    def is_footer_visible(self) -> bool:
        """Gets value indicating that a footer placeholder is present. Read."""
        return self._notes_part.has_placeholder('ftr')

    @property
    def is_slide_number_visible(self) -> bool:
        """Gets value indicating that a page number placeholder is present. Read."""
        return self._notes_part.has_placeholder('sldNum')

    @property
    def is_date_time_visible(self) -> bool:
        """Gets value indicating that a date-time placeholder is present. Read."""
        return self._notes_part.has_placeholder('dt')

    @property
    def is_header_visible(self) -> bool:
        """Gets value indicating that a header placeholder is present. Read."""
        return self._notes_part.has_placeholder('hdr')

    # --- Interface cast properties ---

    @property
    def as_i_base_handout_notes_slide_header_footer_manag(self) -> IBaseHandoutNotesSlideHeaderFooterManag:
        return self

    @property
    def as_i_base_slide_header_footer_manager(self) -> IBaseSlideHeaderFooterManager:
        return self

    @property
    def as_i_base_header_footer_manager(self) -> IBaseHeaderFooterManager:
        return self

    # --- Visibility setters ---

    def set_footer_visibility(self, is_visible: bool) -> None:
        """Modifies footer placeholder visibility."""
        if is_visible:
            self._notes_part.add_placeholder('ftr')
        else:
            self._notes_part.remove_placeholder('ftr')

    def set_slide_number_visibility(self, is_visible: bool) -> None:
        """Modifies page number placeholder visibility."""
        if is_visible:
            self._notes_part.add_placeholder('sldNum')
        else:
            self._notes_part.remove_placeholder('sldNum')

    def set_date_time_visibility(self, is_visible: bool) -> None:
        """Modifies date-time placeholder visibility."""
        if is_visible:
            self._notes_part.add_placeholder('dt')
        else:
            self._notes_part.remove_placeholder('dt')

    def set_header_visibility(self, is_visible: bool) -> None:
        """Modifies header placeholder visibility."""
        if is_visible:
            self._notes_part.add_placeholder('hdr')
        else:
            self._notes_part.remove_placeholder('hdr')

    # --- Text setters ---

    def set_footer_text(self, text: str) -> None:
        """Assigns text content to the footer placeholder."""
        self._notes_part.set_placeholder_text('ftr', text)

    def set_date_time_text(self, text: str) -> None:
        """Assigns text content to the date-time placeholder."""
        self._notes_part.set_placeholder_text('dt', text)

    def set_header_text(self, text: str) -> None:
        """Assigns text content to the header placeholder."""
        self._notes_part.set_placeholder_text('hdr', text)
