from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBaseSlide import IBaseSlide

if TYPE_CHECKING:
    from .IDrawingGuidesCollection import IDrawingGuidesCollection
    from .IMasterLayoutSlideCollection import IMasterLayoutSlideCollection
    from .IMasterSlideHeaderFooterManager import IMasterSlideHeaderFooterManager
    from .ISlide import ISlide
    from .ITextStyle import ITextStyle

class IMasterSlide(IBaseSlide, ABC):
    """Represents a master slide in a presentation."""




    @property
    def layout_slides(self) -> IMasterLayoutSlideCollection:
        """Returns the collection of child layout slides for this master slide. Read-only ."""
        ...








