from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBaseSlide import IBaseSlide

if TYPE_CHECKING:
    from .INotesSlideHeaderFooterManager import INotesSlideHeaderFooterManager
    from .ISlide import ISlide
    from .ITextFrame import ITextFrame

class INotesSlide(IBaseSlide, ABC):
    """Represents a notes slide in a presentation."""
    @property
    def header_footer_manager(self) -> INotesSlideHeaderFooterManager:
        """Returns HeaderFooter manager of the notes slide. Read-only ."""
        ...

    @property
    def notes_text_frame(self) -> ITextFrame:
        """Returns a TextFrame with notes' text if there is one. Read-only ."""
        ...

    @property
    def parent_slide(self) -> ISlide:
        """Returns a ParentSlide Read-only ."""
        ...

    @property
    def as_i_base_slide(self) -> IBaseSlide:
        """Allows to get base IBaseSlide interface. Read-only ."""
        ...

