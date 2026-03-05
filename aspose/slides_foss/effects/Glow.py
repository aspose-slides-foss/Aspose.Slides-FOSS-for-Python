from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IGlow import IGlow
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from .._internal.pptx.slide_part import SlidePart

class Glow(IGlow, IImageTransformOperation):
    """Represents a Glow effect, in which a color blurred outline is added outside the edges of the object."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def radius(self) -> float:
        """Radius. Read/write ."""
        val = self._element.get('rad')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @radius.setter
    def radius(self, value: float):
        self._element.set('rad', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def color(self) -> IColorFormat:
        """Color format. Read-only ."""
        from ..ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(self._element, self._slide_part, self._parent_slide)
        return cf

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

