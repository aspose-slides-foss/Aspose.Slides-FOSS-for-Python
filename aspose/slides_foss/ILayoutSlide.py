from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBaseSlide import IBaseSlide

if TYPE_CHECKING:
    from .IDrawingGuidesCollection import IDrawingGuidesCollection
    from .ILayoutPlaceholderManager import ILayoutPlaceholderManager
    from .ILayoutSlideHeaderFooterManager import ILayoutSlideHeaderFooterManager
    from .IMasterSlide import IMasterSlide
    from .ISlide import ISlide
    from .SlideLayoutType import SlideLayoutType

class ILayoutSlide(IBaseSlide, ABC):
    """Represents a layout slide."""


    @property
    def master_slide(self) -> IMasterSlide:
        """Returns or sets the master slide for a layout. Read/write ."""
        ...

    @master_slide.setter
    def master_slide(self, value: IMasterSlide):
        ...

    @property
    def layout_type(self) -> SlideLayoutType:
        """Returns layout type of this layout slide. Read-only ."""
        ...






