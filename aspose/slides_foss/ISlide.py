from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IBaseSlide import IBaseSlide

if TYPE_CHECKING:
    from .IComment import IComment
    from .IImage import IImage
    from .ILayoutSlide import ILayoutSlide
    from .INotesSlideManager import INotesSlideManager
    from .ISlideHeaderFooterManager import ISlideHeaderFooterManager

class ISlide(IBaseSlide, ABC):
    """Represents a slide in a presentation."""

    @property
    def slide_number(self) -> int:
        """Returns a number of slide. Index of slide in collection is always equal to SlideNumber - 1. Read/write ."""
        ...

    @slide_number.setter
    def slide_number(self, value: int):
        ...

    @property
    def hidden(self) -> bool:
        """Determines whether the specified slide is hidden during a slide show. Read/write ."""
        ...

    @hidden.setter
    def hidden(self, value: bool):
        ...

    @property
    def layout_slide(self) -> ILayoutSlide:
        """Returns or sets the layout slide for the current slide. Read/write ."""
        ...

    @layout_slide.setter
    def layout_slide(self, value: ILayoutSlide):
        ...

    @property
    def notes_slide_manager(self) -> INotesSlideManager:
        """Allow to access notes slide, add and remove it. Read-only ."""
        ...
    def get_slide_comments(self, author) -> list[IComment]:
        ...
    def remove(self) -> None:
        ...

