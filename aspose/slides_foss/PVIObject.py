from __future__ import annotations
from typing import TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .IPresentation import IPresentation

class PVIObject(ISlideComponent, IPresentationComponent):
    """Encapsulates basic service infrastructure for objects can be a subject of property value inheritance."""
    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        """Allows to get base IPresentationComponent interface. Read-only ."""
        return self

    @property
    def slide(self) -> IBaseSlide:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide
        return None

    @property
    def presentation(self) -> IPresentation:
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        return None
