from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IGradientStop import IGradientStop

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat
    from ._internal.pptx.slide_part import SlidePart


class GradientStop(PVIObject, ISlideComponent, IPresentationComponent, IGradientStop):
    """Represents a gradient format."""

    def _init_internal(self, gs_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._gs_element = gs_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def position(self) -> float:
        """Returns or sets the position (0..1) of a gradient stop. Read/write."""
        if not hasattr(self, '_gs_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        pos = self._gs_element.get('pos', '0')
        return int(pos) / 100000.0

    @position.setter
    def position(self, value: float):
        if not hasattr(self, '_gs_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._gs_element.set('pos', str(int(round(value * 100000))))
        self._save()

    @property
    def color(self) -> IColorFormat:
        """Returns the color of a gradient stop. Read-only."""
        if not hasattr(self, '_gs_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(self._gs_element, self._slide_part, self._parent_slide)
        return cf
