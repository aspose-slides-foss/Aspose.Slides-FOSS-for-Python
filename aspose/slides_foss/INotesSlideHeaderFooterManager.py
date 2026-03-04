from __future__ import annotations
from abc import ABC, abstractmethod

class INotesSlideHeaderFooterManager(ABC):
    """Represents manager which holds behavior of the notes slide placeholders, including header placeholder."""
    @property
    def as_i_base_handout_notes_slide_header_footer_manag(self) -> IBaseHandoutNotesSlideHeaderFooterManag:
        """Returns IBaseHandoutNotesSlideHeaderFooterManag interface."""
        ...
