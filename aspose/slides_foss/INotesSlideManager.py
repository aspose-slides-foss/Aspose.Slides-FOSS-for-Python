from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .INotesSlide import INotesSlide

class INotesSlideManager(ABC):
    """Notes slide manager."""
    @property
    def notes_slide(self) -> INotesSlide:
        """Returns the notes slide for the current slide. Returns null if slide doesn't have notes slide. Read-only ."""
        ...
    def add_notes_slide(self) -> INotesSlide:
        ...
    def remove_notes_slide(self) -> None:
        ...

